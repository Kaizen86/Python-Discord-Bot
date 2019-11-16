from commands.modules.common import *
from traceback import format_exc #for error handling

from io import BytesIO #beauty, protecc
from random import randint #mca, beauty, protecc
from requests import get as get_request #beauty, protecc
from PIL import Image, ImageOps, ImageEnhance #mca, beauty, protecc, deepfry

#image manipulation commands
async def beauty(passedvariables):
	#include all the required variables
	message = passedvariables["message"]
	commandprefix = passedvariables["commandprefix"]
	client = passedvariables["client"]
	core_files_foldername = passedvariables["core_files_foldername"]

	usage = "Usage: "+commandprefix+"beauty <mention>"
	array = message.content.split()
	try:
			userid = getUserId(array[1])
	except:
			error = format_exc()
			if "IndexError" in error:
				await message.channel.send(usage)
				return #end command
			else:
				await message.channel.send("""Error while formatting mention into user id.
`"""+error+"`")
				consoleOutput(error)
				return
	background = Image.open(core_files_foldername+"/images/beauty.jpg").convert("RGBA") #original meme image

	try:
		user = await client.fetch_user(userid) #retrieve information of user
	except:
		error = format_exc()
		if "Not Found" in error:
			await message.channel.send("No user exists with the ID "+userid)
			consoleOutput("No user exists with the ID "+userid)
		else:
			await message.channel.send("""Unknown error!
`"""+error+"`")
			consoleOutput("""Unknown error!
"""+error)
		return

	response = get_request(user.avatar_url) #get the image data from the avatar_url and store that into response.
	foreground = Image.open(BytesIO(response.content)).convert("RGBA") #parse response into Image object. This contains the pfp.

	resized = foreground.resize((131,152)) #make foreground the correct size for the target area
	background.paste(resized, (386, 37), resized) #move the foreground into the correct area for the first target area
	resized = foreground.resize((128,154)) #make foreground the correct size for the target area
	background.paste(resized, (389, 338), resized) #move the foreground into the correct area for the second target area

	await uploadImageFromObject(background,message)
async def protecc(passedvariables):
	#include all the required variables
	message = passedvariables["message"]
	commandprefix = passedvariables["commandprefix"]
	client = passedvariables["client"]
	core_files_foldername = passedvariables["core_files_foldername"]

	usage = "Usage: "+commandprefix+"protecc <mention>"
	array = message.content.split()
	try:
		userid = getUserId(array[1])
	except:
		error = format_exc()
		if "IndexError" in error:
			await message.channel.send(usage)
			return #end command
		else:
			await message.channel.send("""Error while formatting mention into user id.
`"""+error+"`")
			consoleOutput(error)
			return
	background = Image.open(core_files_foldername+"/images/protecc.png").convert("RGBA") #original meme image

	try:
		user = await client.fetch_user(userid) #retrieve information of user
	except:
		error = format_exc()
		if "Not Found" in error:
			await message.channel.send("No user exists with the ID "+userid)
			consoleOutput("No user exists with the ID "+userid)
		else:
			await message.channel.send("""Unknown error!
`"""+error+"`")
			consoleOutput("""Unknown error!
"""+error)
		return
	response = get_request(user.avatar_url) #get the image data from the avatar_url and store that into response.
	foreground = Image.open(BytesIO(response.content)).convert("RGBA") #parse response into Image object. This contains the pfp.

	foreground = foreground.resize((124,170)).rotate(-24, expand=1) #rotate foreground and make the correct size for the target area
	background.paste(foreground, (382, 129), foreground) #move the foreground into the correct area for the target area

	await uploadImageFromObject(background,message)
async def deepfry(passedvariables):
	#include all the required variables
	message = passedvariables["message"]
	commandprefix = passedvariables["commandprefix"]
	client = passedvariables["client"]
	core_files_foldername = passedvariables["core_files_foldername"]
	img = passedvariables["previous_img"]

	if not img:
		await message.channel.send("Please post an image in the channel for me to deepfry.")
		consoleOutput("No image has been posted. Aborting.")
		return

	await message.channel.send("Frying the image. This may take a second...")

	#save image from Discord
	extension = img.filename[img.filename.rfind("."):] #get extension from filename
	filename = str(randint(1,99999999))+extension #generate unique id with the extension
	await img.save(filename, seek_begin=True) #save under unique filename to disk
	consoleOutput(filename)
	#and then load it again!
	img = Image.open(filename)

	#https://github.com/Ovyerus/deeppyer/blob/master/deeppyer.py  lines 83-104 (modified)
	# Crush image to hell and back
	img = img.convert('RGB')
	width, height = img.width, img.height
	img = img.resize((int(width ** .75), int(height ** .75)), resample=Image.LANCZOS)
	img = img.resize((int(width ** .88), int(height ** .88)), resample=Image.BILINEAR)
	img = img.resize((int(width ** .9), int(height ** .9)), resample=Image.BICUBIC)
	img = img.resize((width, height), resample=Image.BICUBIC)
	img = ImageOps.posterize(img, 4)
	# Generate red and yellow overlay for classic deepfry effect
	r = img.split()[0]
	r = ImageEnhance.Contrast(r).enhance(2.0)
	r = ImageEnhance.Brightness(r).enhance(1.5)
	RED = (254, 0, 2)
	YELLOW = (255, 255, 15)
	r = ImageOps.colorize(r, RED, YELLOW)
	# Overlay red and yellow onto main image and sharpen the hell out of it
	img = Image.blend(img, r, 0.75)
	img = ImageEnhance.Sharpness(img).enhance(100.0)

	#upload finished image
	await uploadImageFromObject(img,message)
	delete_file(filename)

