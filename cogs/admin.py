from discord.ext import commands
from discord import Status
from traceback import format_exc
from os import _exit as force_exit
from datetime import datetime

#Return the time as well as the date. Used in the log functions
def log(string): return datetime.now().strftime("%m/%d %H:%M:%S ")

class AdminCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.shutdown.description = "Shuts the bot down."

	@commands.command()
	async def reloadallext(self, ctx):
		def log(string): print(time()+"[Admin.reloadallext] "+str(string))
		log("###Initiating reload of all extensions.###")
		msg = await ctx.send("Reloading all extensions...")
		#We have to make a copy to avoid changing the thing we are iterating over as we go
		extensions = self.bot.extensions.copy()
		output = ""
		for extension in extensions:
			try: self.bot.reload_extension(extension)
			except: success = False
			else: success = True
			output += "\n\t{0}:\t[{1}]".format(extension, "OK" if success else "ERR")
		await msg.edit(content=msg.content+output+"\nOperation finished.")
		log(output)
		log("###Reload completed.###")
		
	"""

	@commands.command()
	async def reloadext(self, ctx, ext: str):
		msg = await ctx.send("Reloading extension {}... ".format(ext))
		#We have to make a copy to avoid changing the thing we are iterating over as we go
		extensions = self.bot.extensions.copy()
		if ext in extensions:
			print(time()+" EXTENSION '{}' RELOAD INITIATED")
			try: self.bot.reload_extension(ext)
			except: success = False
			else: success = True
			output = "[{}]".format("OK" if success else "ERR")
			await msg.edit(content=msg.content+output+"\nOperation finished.")
		else: await msg.edit(content=msg.content+output+"\nNo such extension was found.")

	@commands.command()
	async def loadext(self, ctx, *, ext: str):
		msg = await ctx.send("Loading extension {}... ".format(ext))
		print("Loading extension "+ext)
		output = ""
		try: self.bot.load_extension(ext)
		except:
			success = False
			output += format_exc()
		else: success = True
		output = "[{}]".format("OK" if success else "ERR")
		await msg.edit(content=msg.content+output+"\nOperation finished.")
	"""

	@commands.command()
	async def shutdown(self, ctx):
		await ctx.send("Okay, see you later.")
		#Disconnect from all voice clients
		vc_count = 0
		for vc in self.bot.voice_clients:
			await vc.disconnect()
			vc_count += 1
		#if vc_count == 0: await ctx.send("No active voice clients.")
		#else: await ctx.send("Disconnected from {0} voice clients.".format(vc_count))
		#Set visibility to invisible
		await self.bot.change_presence(status=Status.invisible)
		#Quit program
		force_exit(0)

def setup(bot):
	bot.add_cog(AdminCog(bot))
