from discord.ext import commands
from datetime import datetime

def time():
	"""Returns a formatted timestamp suitable for use in log functions"""
	return datetime.now().strftime("%m/%d %H:%M:%S ")

class RoleManagerCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command
	async def colour(self, ctx, *, hexcode: str):
		def log(string):
			print(time() + "[RoleManage.colour] " + str(string))

def setup(bot):
	bot.add_cog(RoleManagerCog()(bot))
