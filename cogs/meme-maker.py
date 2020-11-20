from discord.ext import commands
from discord import utils
import asyncio
from datetime import datetime
from os import path, listdir
import numpy
from PIL import Image
from io import BytesIO
import requests
from discord import File

#Return the time as well as the date. Used in the log functions
def time(): return datetime.now().strftime("%m/%d %H:%M:%S ")

class PerspectiveTransformHelper:
	#No way I would have worked this one out by myself.
	#https://stackoverflow.com/questions/14177744/how-does-perspective-transformation-work-in-pil
	def find_coeffs(pb, pa):
	    matrix = []
	    for p1, p2 in zip(pa, pb):
	        matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
	        matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])

	    A = numpy.matrix(matrix, dtype=numpy.float)
	    B = numpy.array(pb).reshape(8)

	    res = numpy.dot(numpy.linalg.inv(A.T * A) * A.T, B)
	    return numpy.array(res).reshape(8)

	def transform(template, content, transform_coordinates):
		"""Takes 2 PIL.Image objects (the meme template and the content to apply) as well as perspective transform coordinates.
		Returns an image where the content is transformed and overlayed behind the template image.

		The transform coordinates consist of a list of 4 tuples. The tuples are pixel coordinates for where each corner in
		the content should be relocated to. The order is top-left, top-right, bottom-right, bottom-left."""
		def log(string): return #Disabled for brevity, I am done with debugging it for now. #print(time()+"[MemeMaker.PerspectiveTransformHelper] "+str(string))

		#Upscale content to the template size
		content = content.resize(template.size)

		log("Compute coefficients")
		x,y = content.size
		coeffs = PerspectiveTransformHelper.find_coeffs( #Not entirely sure why I need to retype the class name. Apparently it can't find it.
			#Define the corners of the image
	        [(0, 0), (x, 0), (x, y), (0, y)],
			#Define where the content corners should go,
			#Taken as pixel coordinates from the template which is why I upscaled the content earlier
	        transform_coordinates)

		log("Transform content image")
		resized_content = content.transform(
			content.size,
			Image.PERSPECTIVE, coeffs,
		    Image.BICUBIC)
		#resized_content.show() #debugging

		log("Overlaying template onto content")
		output = Image.alpha_composite(resized_content, template)
		log("Done")
		return output

class MemeMaker(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.path = path.dirname(__file__)+"/"
		self.templates = {}
		directory = self.path+"meme-maker-assets/"
		for file in listdir(directory):
			#Load each image into a dictionary with an appropriate key
			#Example key: testimage.png --> ["testimage"]
			key = file[:file.index(".")]
			try: self.templates[key] = Image.open(directory+file).convert("RGBA")
			except: pass #Ignore errors, it was probably not an image file we loaded

	@asyncio.coroutine
	async def perform_transform(self, template_key, content, transform):
		#Just to save me from pasting it into every command that uses perspective transforms
		image_binary = BytesIO()
		PerspectiveTransformHelper.transform(
			self.templates[template_key],
			content,
			transform
		).save(image_binary, "PNG")
		image_binary.seek(0)
		return image_binary

	@asyncio.coroutine
	async def retrieve_image(self, ctx, url):
		def log(string): print(time()+"[MemeMaker.retrieve_image] "+str(string))
		if url == None:
			#Check for attachment
			if len(ctx.message.attachments) > 0:
				attachment = ctx.message.attachments[0] #Only pick the first if for some reason they sent multiple
				#Is it an image? Check for the image dimensions
				if attachment.height > 0:
					#It's confirmed to be an image. Extract the extension and load it as an Image object
					name = attachment.filename
					extension = name[name.index(".")+1:]
					log("Image has {} extension...".format(extension))
					data = await attachment.read()
					log("Downloaded content.")
					try: return Image.open(BytesIO(data)).convert("RGBA")
					except:
						await ctx.send("Unable to load image.")
						return
				else:
					await ctx.send("Attachment is not an image.")
					return
			else:
				#Neither a URL nor attachment was provided
				await ctx.send("No image was provided.")
				return
		else:
			#Attempt to download the image
			log("Image type is url.")
			response = requests.get(url)
			try: return Image.open(BytesIO(response.content)).convert("RGBA")
			except:
				await ctx.send("Unable to load image from URL.")
				return

	@commands.command()
	async def opinion(self, ctx, url: str = None): #Can either be a URL or a ctx.message.attachment. If both are None, yell at them
		"""I would like your honest opinion... if you would.
		Accepts either a URL or a direct image attachment."""
		def log(string): print(time()+"[MemeMaker.opinion] "+str(string))
		template_key = "honest-opinion" #What meme template should be used for this command?

		#Extract the image object from the message
		log("Getting image")
		image = await self.retrieve_image(ctx, url)
		if image == None:
			log("No image?")
			await ctx.send("Apologies, but that doesn't seem to have an image.")
			return
		#Process the image
		log("Processing")
		image_binary = await self.perform_transform(template_key, image, [(290,175), (557,163), (572,350), (311,374)])
		#Send it
		log("Sending")
		await ctx.send(file=File(fp=image_binary, filename=template_key+".png"))

def setup(bot):
	bot.add_cog(MemeMaker(bot))
