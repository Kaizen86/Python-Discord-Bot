from discord.ext import commands

class VoiceCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def test(self, ctx):
		await ctx.send("module is wip")
		await ctx.send(ctx.voice_client is not None)

	@test.before_invoke
	async def ensure_voice(self, ctx):
		if ctx.voice_client is None:
			if ctx.author.voice:
				await ctx.author.voice.channel.connect()
			else:
				await ctx.send("You are not connected to a voice channel.")
				raise commands.CommandError("Author not connected to a voice channel.")
		elif ctx.voice_client.is_playing():
			ctx.voice_client.stop()

def setup(bot):
    bot.add_cog(VoiceCog(bot))






"""
print(dir(ctx.author.voice.channel))
await ctx.send("sent output to term.")
return
if ctx.author.voice is not None:
	return await ctx.voice_client.move_to(ctx.author.channel)
else: await ctx.voice_client.connect()
"""
