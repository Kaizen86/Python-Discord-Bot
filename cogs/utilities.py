import discord
from discord.ext import commands
import asyncio
from datetime import datetime

#Return the time as well as the date. Used in the log functions
def time(): return datetime.now().strftime("%m/%d %H:%M:%S ")

class Utilities(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def avatar(self, ctx, *, user: discord.Member = None):
		"""Gets somebody's avatar
		You must specify a user by pinging them.
		Example: .avatar @Elizabeth"""
		if not user:
			await ctx.send("No user specified")
			return

		embed = discord.Embed(title="Avatar for "+user.name+"#"+user.discriminator)
		url = user.avatar_url[:user.avatar_url.index("?")] #Strip any query strings from the url to provide the maximum quality image
		embed.set_image(url=url)
		await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(Utilities(bot))
