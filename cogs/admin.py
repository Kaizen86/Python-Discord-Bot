from discord.ext import commands
from discord import Status
from traceback import format_exc
from os import _exit as force_exit
from datetime import datetime

#Return the time as well as the date. Used in the log functions
def time(): return datetime.now().strftime("%m/%d %H:%M:%S ")

class AdminCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def reloadallext(self, ctx):
		"""Reloads all extensions"""
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

	@commands.command()
	async def reloadext(self, ctx, *, ext: str):
		"""Reloads a specific extension
		Must be in the format 'cogs.extensionname'."""
		msg = await ctx.send("Reloading extension {}... ".format(ext))
		print("Reloading extension "+ext)
		error = "Operation finished."
		success = False
		try: self.bot.reload_extension(ext)
		except:
			error = "```{}```".format(format_exc())
		else: success = True
		await msg.edit(content="{0} [{1}]\n{2}".format(msg.content, "OK" if success else "ERR", error))

	@commands.command()
	async def loadext(self, ctx, *, ext: str):
		"""Loads a specific extension
		Must be in the format 'cogs.extensionname'."""
		msg = await ctx.send("Loading extension {}... ".format(ext))
		print("Loading extension "+ext)
		error = "Operation finished."
		success = False
		try: self.bot.load_extension(ext)
		except commands.errors.ExtensionAlreadyLoaded:
			error = "This extension is already loaded, please use reloadext."
		except:
			error = "```{}```".format(format_exc())
		else: success = True
		await msg.edit(content="{0} [{1}]\n{2}".format(msg.content, "OK" if success else "ERR", error))

	@commands.command()
	async def shutdown(self, ctx):
		"""Shuts the bot down as fast as possible"""
		await ctx.send("I await the day we meet again.")
		#Disconnect from all voice clients
		vc_count = 0
		for vc in self.bot.voice_clients:
			await vc.disconnect()
			vc_count += 1
		if vc_count > 0: await ctx.send("Disconnected from {0} voice clients.".format(vc_count))
		#Set visibility to invisible for an immediate effect
		await self.bot.change_presence(status=Status.invisible)
		#Quit program
		force_exit(0)

def setup(bot):
	bot.add_cog(AdminCog(bot))
