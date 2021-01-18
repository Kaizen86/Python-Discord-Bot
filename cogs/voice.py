from discord.ext import commands
from discord import Emoji
class VoiceCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	async def BotInSameVoiceChannelAsMember(self, ctx, member):
		if member.voice: #Is the summoning user in a vc?
			if ctx.voice_client is not None: #Are we in a vc?
				#Yes. Do the channel IDs match?
				if member.voice.channel.id == ctx.voice_client.channel.id: return True #yes.
		#In all other cases, return False.
		return False

	@commands.command()
	async def join(self, ctx):
		"""Join the voice channel you are in
		I will try to connect to the voice channel you are currently in and then add a reaction to your message to say if I suceeded."""
		if ctx.voice_client is not None: await ctx.message.add_reaction('✅') #React with a check if we suceeded in joining the vc
		else: #Otherwise react with a cross
			await ctx.message.add_reaction('❎')
			return

	"""
	@commands.command()
	async def play(self, ctx, url: str):
		player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
		ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
		await ctx.send('Now playing: {}'.format(player.title))
	"""

	@commands.command()
	async def leave(self, ctx):
		if await self.BotInSameVoiceChannelAsMember(ctx, ctx.author):
			await ctx.voice_client.disconnect()
			#This is the only way I was able to get message reactions to work properly and is probably the intended way.
			#Kind of annoys me having emoji in source code as it sticks out like a sore thumb but it can't be helped.
			await ctx.message.add_reaction('✅')
		else: await ctx.send("lol no")


	# discord.on_voice_state_update(member, before, after) #use this to detect members leaving voice calls and decide whether that should prompt us to leave as well. no point being connected if nobody else is.

	@join.before_invoke
	#@play.before_invoke
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
		else: #They are not in a vc, inform them.
			await ctx.send("You are not connected to a voice channel.")
def setup(bot):
    bot.add_cog(VoiceCog(bot))
