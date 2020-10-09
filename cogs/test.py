import discord
from discord.ext import commands

class TestCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def test(self, ctx, *, number: int):
		if number is None: await ctx.send("Please give a number")
		else: await ctx.send(number)

def setup(bot):
    bot.add_cog(TestCog(bot))
