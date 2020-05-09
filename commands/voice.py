from commands.modules.common import *
from traceback import format_exc #for error handling
from discord import FFmpegPCMAudio #used by everything except disconnect

import gtts #speak
from time import sleep #speak
from random import randint #speak
from ast import literal_eval #playyt
import youtube_dl #playyt

async def connectvc(voice_clients, author):
	#check if we are already in the voice channel that the requesting user is.
	for vc in voice_clients:
		if vc.guild == author.guild:
			if vc.channel == author.voice.channel:
				#same server, same channel, use that connection
				consoleOutput("Found existing voice channel connection.")
				break
			else:
				#same server, different channel.
				consoleOutput("Reconnect to different channel within the same server.")
				await vc.disconnect() #we must first disconnect the vc
				vc = await author.voice.channel.connect() #then we can make a new connection
				consoleOutput("Success!")
				break
	else: #we are not already in the vc, so we join it.
		consoleOutput("Connecting...")
		vc = await author.voice.channel.connect()
		consoleOutput("Success!")
	return vc

#voice channel commands
async def vc_rickroll(passedvariables):
	#include all the required variables
	message = passedvariables["message"]
	core_files_foldername = passedvariables["core_files_foldername"]
	client = passedvariables["client"]

	#confirm that the user is in a voice channel
	if not message.author.voice:
		await message.channel.send("You are not in a voice channel.")
		consoleOutput("User is not in channel.")
		return

	#either create a voice client or use an existing one
	vc = await connectvc(client.voice_clients, message.author)

	#load audio file from disk
	audio = FFmpegPCMAudio(core_files_foldername+"/audio/rickroll.mp3", executable='ffmpeg')
	audio.volume = 5 #set audio level to 5 out of... something. probably 10.
	consoleOutput("Opened audio file.")

	vc.play(audio) #and finally, play the audio file.
	await message.channel.send("Rickrolling.")
	consoleOutput("Rickrolling.")

async def vc_playyt(passedvariables):
	#include all the required variables
	message = passedvariables["message"]
	client = passedvariables["client"]
	commandprefix = passedvariables["commandprefix"]
	core_files_foldername = passedvariables["core_files_foldername"]

	usage = commandprefix+"play <url/search term>"

	#confirm that the user is in a voice channel
	if not message.author.voice:
		await message.channel.send("You are not in a voice channel.")
		consoleOutput("User is not in channel.")
		return

	#either create a voice client or use an existing one
	vc = await connectvc(client.voice_clients, message.author)

	try:
		url = message.content[len(commandprefix)+5:] #4 for the word, 1 more for a space.
	except:
		await message.channel.send("""Please provide a YouTube video URL.
"""+usage)
		return

	#instead of sending a message every time something happens, let's just update one message.
	outputmsg = await message.channel.send("Gathering video metadata...")

	#initialise youtube downloader instance with options
	opts = {
		"retries":50, #Number of attempts of connecting to stream before abandoning
		"reconnect":1, #Attempt to reconnect to the stream
		"reconnect_streamed":1, #Attempt to reconnect to the stream
		"reconnect_delay_max":10, #Attempt to reconnect to the stream
		"socket_timeout":10.0 #Number of seconds before giving up on a connection.
	}
	ydl = youtube_dl.YoutubeDL(opts)
	#override information output functions with our custom log function
	ydl.to_stdout = consoleOutput
	ydl.to_stderr = consoleOutput
	try:
		data = ydl.extract_info(url, download=False) #extract metadata from video
	except:
		#url was not provided; rather a search term.
		data = ydl.extract_info("ytsearch:"+url, download=False)["entries"][0] #extract metadata from first video result
		await outputmsg.edit(content=outputmsg.content+"\nPlaying '{}'.".format(data["title"]))

	#sift through the barrage of data returned
	url = None #reset url variable
	for format in data["formats"]:
		if format["ext"] == "m4a":
			url = format["url"]
			break
	if not url:
		await outputmsg.edit(content=outputmsg.content+"\nUnable to get audio from video.")
		consoleOutput("Unable to get audio version of video. No available formats are M4A.")
		return

	audio = FFmpegPCMAudio(url, executable='ffmpeg') #open stream
	audio.volume = 5 #set audio level to 5 out of... something. probably 10.
	await outputmsg.edit(content=outputmsg.content+"\nOpened audio stream.")
	consoleOutput("Opened audio stream.")

	vc.play(audio) #and finally, play the audio file.
	await outputmsg.edit(content=outputmsg.content+"\nPlaying.")
	consoleOutput("Success.")

async def vc_speak(passedvariables):
	#include all the required variables
	message = passedvariables["message"]
	client = passedvariables["client"]
	commandprefix = passedvariables["commandprefix"]
	core_files_foldername = passedvariables["core_files_foldername"]

	usage = commandprefix+"speak <text>"

	#confirm that the user is in a voice channel
	if not message.author.voice:
		await message.channel.send("You are not in a voice channel.")
		consoleOutput("User is not in channel.")
		return

	#either create a voice client or use an existing one
	vc = await connectvc(client.voice_clients, message.author)

	text = message.content[len(commandprefix)+6:] #5 for the word, 1 more for a space.
	await message.delete() #we can now remove the message for stealth purposes.
	randomid = randint(0,99999999)
	gtts.gTTS(text, lang="en-uk", slow=False).save(str(randomid)+".mp3")

	audio = FFmpegPCMAudio(str(randomid)+".mp3", executable='ffmpeg') #open file
	audio.volume = 5 #set audio level to 5 out of... something. probably 10.
	consoleOutput("Opened audio file.")

	vc.play(audio) #and finally, play the audio file.
	consoleOutput("Playing audio.")
	for i in range(1000): #since we cant know when it's done with the file, repeatedly try to delete it until it works. this is a massive bodge, but it works. capped at 1000 attempts just in case.
		sleep(1)
		try:
			delete_file(str(randomid)+".mp3")
			consoleOutput(F"Deleted temporary audio file '{randomid}.mp3' after {i} seconds.")
			break #stop trying
		except Exception as err: pass #ignore errors and keep trying.

async def vc_disconnect(passedvariables):
	message = passedvariables["message"]
	client = passedvariables["client"]

	#confirm that the user is in a voice channel
	if not message.author.voice:
		await message.channel.send("You are not in a voice channel.")
		consoleOutput("User is not in channel.")
		return

	vc = await connectvc(client.voice_clients, message.author)
	await vc.disconnect()
	consoleOutput("Disconnected.")
	await message.channel.send("Disconnected.")
