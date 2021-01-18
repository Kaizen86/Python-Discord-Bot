from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL

class Voice(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	async def BotInSameVoiceChannelAsMember(self, ctx, member):
		"""Given a member object, check if they are connected to the same voice channel as us."""
		if member.voice: #Is the summoning user in a vc?
			if ctx.voice_client is not None: #Are we in a vc?
				#Yes. Do the channel IDs match?
				if member.voice.channel.id == ctx.voice_client.channel.id: return True #Yes.
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

	@commands.command()
	async def play(self, ctx, *, url: str = None):
		"""Plays a youtube video from a link
		You can only give one link.
		play <link>"""
		if not url:
			await ctx.send("Please, you must give me a link to the song.")
			return
		elif not await self.BotInSameVoiceChannelAsMember(ctx, ctx.author):
			await ctx.send("You are not in the same voice call as me.")
			return
		#Credit to stackoverflow for this one https://stackoverflow.com/questions/63024148/discord-music-bot-voiceclient-object-has-no-attribute-create-ytdl-player
		#Adapted a bit, though.
		ydl_opts = {'format': 'bestaudio', 'noplaylist':'True'}
		ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

		if ctx.voice_client is not None:
			if ctx.voice_client.is_playing(): await ctx.voice_client.stop()

		with YoutubeDL(ydl_opts) as ydl:
			info = ydl.extract_info(url, download=False)
		URL = info['formats'][0]['url']
		ctx.voice_client.play(FFmpegPCMAudio(URL, **ffmpeg_options))
		await ctx.send('Playing song')

	#TODO: Add 'search' command

	@commands.command()
	async def stop(self, ctx):
		"""Cancels whatever is playing"""
		if not ctx.voice_client:
			await ctx.send("I am not in a voice call.")
		elif not ctx.voice_client.is_playing():
			await ctx.send("I am not playing anything at the moment.")
		elif not await self.BotInSameVoiceChannelAsMember(ctx, ctx.author):
			await ctx.send("You are not in the same voice call as me.")
		else:
			ctx.voice_client.stop()
			await ctx.send('Stopped playing')

	"""
	@commands.command()
	async def leave(self, ctx):
		if await self.BotInSameVoiceChannelAsMember(ctx, ctx.author):
			await ctx.voice_client.disconnect()
			#This is the only way I was able to get message reactions to work properly and is probably the intended way.
			#Kind of annoys me having emoji in source code as it sticks out like a sore thumb but it can't be helped.
			await ctx.message.add_reaction('✅')
		else: await ctx.send("You are not in the same voice call as me.")
	"""

	#Client has stated that the bot should only leave a vc when everyone disconnects
	@commands.Cog.listener()
	async def on_voice_state_update(self, member, before, after):
		#Detect members leaving voice calls and decide whether that should prompt us to leave as well.
		if member.bot: return #Ignore events coming from bots
		voice = get(self.bot.voice_clients, guild=member.guild)
		if voice is None: return #Are we even in a voice call?
		if voice.channel.id is not before.channel.id: return #Ignore events that are unrelated to our channel
		#Count how many people are still in the channel
		humans = 0
		for member in before.channel.members:
			if not member.bot: humans += 1
		if humans == 0: #All the people have left, so we should leave the call.
			await voice.disconnect()

	@join.before_invoke
	@play.before_invoke
	#@search.before_invoke
	async def ensure_voice(self, ctx):
		if ctx.author.voice: #Is the summoning user in a vc?
			channel = ctx.author.voice.channel
			if ctx.voice_client is not None: #Are we in a vc?
				#We are not, do we have to switch to their channel?
				if channel.id == ctx.voice_client.channel.id: return #No.
				await ctx.guild.change_voice_state(channel=channel) #Yes, switch to theirs.
				return
			#We are not in a vc, therefore we should connect to theirs.
			await channel.connect()
		else: #They are not in a vc, inform them.
			await ctx.send("You are not connected to a voice channel.")

def setup(bot):
    bot.add_cog(Voice(bot))
