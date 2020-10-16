import discord
from discord.ext import commands
from discord import Status
from os import _exit as force_exit

class AdminCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def reloadext(self, ctx):
		msg = await ctx.send("Reloading all extensions...")
		#We have to make a copy to avoid changing the thing we are iterating over as we go
		extensions = self.bot.extensions.copy()
		for extension in extensions:
			self.bot.reload_extension(extension)
			await msg.edit(content=msg.content+"\n\t"+extension)
		await msg.edit(content=msg.content+"\nOperation finished.")

	@commands.command()
	async def shutdown(self, ctx):
		await ctx.send("Shutting bot down...")
		#Disconnect from all voice clients
		vc_count = 0
		for vc in self.bot.voice_clients:
			await vc.disconnect()
			vc_count += 1
		if vc_count == 0: await ctx.send("No active voice clients.")
		else: await ctx.send("Disconnected from {0} voice clients.".format(vc_count))
		#Set visibility to invisible
		await self.bot.change_presence(status=Status.invisible)
		await ctx.send("Goodbye.")
		#Quit program
		force_exit(0)

def setup(bot):
	bot.add_cog(AdminCog(bot))
