import discord
from discord.ext import commands

class Utilities(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(
		usage="[ping]"
	)
	async def avatar(self, ctx, *, user: discord.Member = None):
		"""Gets somebody's avatar.

Specify a user by pinging them."""
		if not user:
			await ctx.send("Sorry, please say who you want to see.")
			return

		embed = discord.Embed(title="Avatar for " + user.name + "#" + user.discriminator)
		# Strip any query strings from the url to provide the maximum quality image
		url = user.avatar_url[:user.avatar_url.index("?")]
		embed.set_image(url=url)
		await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(Utilities(bot))
