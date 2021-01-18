from discord.ext import commands

class VoiceCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@test.before_invoke
	@play.before_invoke
	async def ensure_voice(self, ctx):
		if ctx.author.voice: #Is the summoning user in a vc?
			channel = ctx.author.voice.channel
			if ctx.voice_client is not None: #Are we in a vc?
				#Yes. Do we have to switch to their channel?
				if channel.id == ctx.voice_client.channel.id: return #No.
				await ctx.guild.change_voice_state(channel=channel) #Yes, switch to theirs.
				return
			#We are not in a vc, therefore we should connect to theirs.
			await channel.connect()
		else: #They are not in a vc, inform them and raise an appropriate exception.
			await ctx.send("You are not connected to a voice channel.")
			raise commands.CommandError("Author not connected to a voice channel.")

	@commands.command()
	async def test(self, ctx):
		"""Developer test command for the voice channel code
		Will try to connect to the voice channel you are currently in and then outputs some nonsense."""
		await ctx.send(ctx.voice_client is not None)
		await ctx.send(str(dir(ctx.voice_client)).replace("_","\_"))

	"""
	@commands.command()
	async def play(self, ctx, url: str):
		player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
		ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
		await ctx.send('Now playing: {}'.format(player.title))
	"""

	#@commands.command()
	#async def leave():

	# discord.on_voice_state_update(member, before, after) #use this to detect members leaving voice calls and decide whether that should prompt us to leave as well. no point being connected if nobody else is.

def setup(bot):
    bot.add_cog(VoiceCog(bot))
