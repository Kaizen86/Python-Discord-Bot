from time import localtime #file logs
from os import listdir #folder existence checks
from os import mkdir #make new folder if needed

def verifyFolderExistence(foldername):
	if foldername not in listdir():
		print("Making '"+foldername+"' folder.")
		mkdir(foldername)
		
time = localtime() #get the time
verifyFolderExistence("logs")
logfilename = "logs\\log_"+str(time[0])+"-"+str(time[1])+"-"+str(time[2])+".txt" #determine which log file we should write to based on the date
def consoleOutput(text, *args, **kwargs): #consoleOutput is encouraged as a replacement of print as it writes everything to a log file.
	#get time and date
	time = localtime()
	#format text to have timestamp
	text = str(time[0])+"/"+str(time[1])+"/"+str(time[2])+" "+str(time[3])+":"+str(time[4])+":"+str(time[5])+": "+text
	#prints to the console
	print(text)
	#write to log
	logfile = open(logfilename,"a")
	logfile.write(text+"\n")
	logfile.close()
	
import discord
from traceback import format_exc #for error handling

#internal
print("\tInternal (1/2)")
from ast import literal_eval #playyt
import youtube_dl #playyt
from io import BytesIO #mca, beauty, protecc
from typing import BinaryIO #rickroll
from os import remove as delete_file #mca, beauty, protecc
from os import listdir #help
from os import _exit as force_exit #shutdown
from random import randint #dice, coin_toss, rps, mca, beauty, protecc
import re #used to remove non-numbers from mentions to extract the user id
from requests import get #mca, beauty, protecc
from subprocess import PIPE as SUB_PIPE #execute
from subprocess import Popen as shell_exec #execute
import shlex #execute
from sys import version_info as python_info #help
from time import sleep #shutdown
#external (3rd party)
print("\tExternal (2/2)")
from discord import FFmpegPCMAudio #rickroll
from discord import PCMVolumeTransformer #rickroll
import pyfiglet #figlet
import nacl #rickroll
from PIL import Image #mca, beauty, protecc
from modules import shadow_translator #translate (i made this one :D)
shadowtranslator = shadow_translator.ShadowTranslator()

#custom error class for comedic purposes in hilariously catastrophic scenarios
class ExcuseMeWhatTheFuckError(Exception):
    pass
def getUserId(string):
	return re.sub("[^0-9]","",string)
	
	
#user commands
async def help(passedvariables):
	#include all the required variables
	message = passedvariables["message"]
	#send help message to dm of user
	await message.author.send("""General Commands
```
These commands do not have a classification.
Display this help.
{0}help
Tests if the bot is working.
{0}test
Rolls a dice with an optional minimum and maximum limits.
{0}dice [minimum] [maximum]
Gives advice on where to find oxygen. In other words, the perfect command.
{0}oxygen
Tosses a coin. That's it.
{0}coin_toss
Reverses the given text.
{0}reverse <text>
Gets information about a mentioned user.
{0}info <mention>
Gets the avatar of a mentioned user.
{0}avatar <mention>
Play a game of rock paper scissors with the bot. (I promise it doesn't cheat)
{0}rps <rock/paper/scissors>
Gets the bot to repeat the input text. The bot will then try and delete your message to make it look real.
{0}say <text>
Gets the number of times the mentioned user has "meeped".
{0}list_meeps <mention>
Generates a minecraft achievement with a random icon, with text based on the input.
{0}mca <text>
This command allow translation to and from Basic Shadow, which is a language invented by <@284415695050244106>.
{0}translate <to/from> <english>
Generates an ASCII art of the input text.
{0}figlet <text>
Generates an ASCII art of the input text.
Deletes a certain number of messages in the same channel that the command was sent.
{0}purge <number of messages>
```""".format(commandprefix))
	await message.author.send("""
Image manipulation commands
```
{0}beauty <mention>
{0}protecc <mention>
```

Voice channel commands
```
Rickrolls the voice channel you are connected to.
{0}rickroll
Plays a youtube video either from a URL or from a search term. Please be aware THIS IS NOT STABLE!!
{0}play <url/search term>
Disconnects the bot from the connected voice channel.
{0}disconnect
```

Criminality Commands
```
These commands control or list the criminality values of a user.
{0}list_crime <mention>
{0}set_crime <mention> <value>
{0}change_crime <mention> <increment value by>
```

Trigger Words
```
These are words that have make the bot do something if you say them.
	"meep"
	"wheatley" AND "moron"
	"pineapple"
	"no u" OR "no you"
	"the more you know"
```

Bot Administration Commands
```
These commands are intended for the bot owners. Accessing them will send a warning to the owner.

Shutdown the bot.
{0}shutdown
Retrieve stored value for user attribute in database.
{0}getuserdata <mention> <attribute>
Update stored value for user attribute in database.
{0}setuserdata <mention> <attribute> <value>
Execute a shell command on the host computer.
{0}execute <shell command>
Reloads the bot configuration files. Useful for applying changes.
{0}reload
```
Created by <@285465719292821506>.
Python version is {1}.{2}""".format(commandprefix,str(python_info.major),str(python_info.minor)))
	await message.channel.send("List of commands sent in DM.")
async def test(passedvariables):
	#include all the required variables
	message = passedvariables["message"]
	await message.channel.send("Yes, <@"+str(message.author.id)+">. This bot is online.")
async def dice(passedvariables):
	#include all the required variables
	message = passedvariables["message"]
	commandprefix = passedvariables["commandprefix"]
	
	usage = "Usage: "+commandprefix+"dice [minimum] [maximum]"
	#get command parameters and allocate into appropriate variables.
	array = message.content.split()
	if len(array) > 1:
		try:
			min = int(array[1])
			max = int(array[2])
		except:
			error = format_exc()
			if "index" in error:
				#in the event that indexing fails (due to no or insufficient parameters, display the usage.
				await message.channel.send(usage)
			elif "invalid literal" in error:
				#in the event that conversion to an integer fails (likely due to text being entered instead of numbers), display this.
				await message.channel.send("""Minimum and maximum values must be numbers.
"""+usage)
			else:
				await message.channel.send("""Unknown error while reading array index.
`"""+error+"`")
				consoleOutput(error)
			return #end command
	else:
		#no parameters were specified, so the defaults are a regular die.
		min = 1
		max = 6

	if min<max:
		#roll the dice
		await message.channel.send("I rolled "+str(randint(min,max)))
	else:
		await message.channel.send("Minimum & maximum must be numbers.")
async def oxygen(passedvariables):
	#include all the required variables
	message = passedvariables["message"]
	await message.channel.send("Look around and you will find it.")
async def coin_toss(passedvariables):
	#include all the required variables
	message = passedvariables["message"]
	result = randint(1,8)
	if result <= 4:
		result = "Tails"
	else:
		result = "Heads"
	await message.channel.send(result+".")
async def reverse(passedvariables):
	#include all the required variables
	message = passedvariables["message"]
	commandprefix = passedvariables["commandprefix"]
	
	usage = "Usage: "+commandprefix+"reverse <text>"
	try:
		#remove command prefix from string we want
		text = message.content[len(commandprefix)+8:] #change according to length of command name + 1 for the space
	except:
		error = format_exc()
		await message.channel.send("""Error while reading text.
`"""+error+"`")
		consoleOutput(error)
		return #end command
	if not text.replace(" ","") == "":
		await message.channel.send(text[::-1]) #mystical string manipulation command to reverse the input
	else:
		await message.channel.send(usage)
async def info(passedvariables):
	#include all the required variables
	message = passedvariables["message"]
	commandprefix = passedvariables["commandprefix"]
	client = passedvariables["client"]
	
	usage = "Usage: "+commandprefix+"info <mention>"
	array = message.content.split()
	try:
		userid = getUserId(array[1])
	except:
		error = format_exc()
		if "IndexError" in error:
			await message.channel.send(usage)
		else:
			await message.channel.send("""Error while formatting mention into user id.
`"""+error+"`")
			consoleOutput(error)
		return #end command

	try:
		user = await client.get_user_info(userid)
	except:
		error = format_exc()
		if "Unknown User" in error:
			await message.channel.send("No user exists with the ID "+userid)
			consoleOutput("No user exists with the ID "+userid)
			return
	embed = discord.Embed(title="Data dump for user "+user.name+"#"+user.discriminator)
	embed.add_field(name="Is a bot", value=user.bot, inline=False)
	embed.add_field(name="Date created", value=user.created_at, inline=False)
	embed.add_field(name="Nickname", value=user.display_name, inline=False)
	embed.add_field(name="Unique ID", value=user.id, inline=False)
	embed.add_field(name="Avatar", value=".", inline=False)
	embed.set_image(url=user.avatar_url)
	await message.channel.send(embed=embed)
async def avatar(passedvariables):
	#include all the required variables
	message = passedvariables["message"]
	commandprefix = passedvariables["commandprefix"]
	client = passedvariables["client"]
	
	usage = "Usage: "+commandprefix+"avatar <mention>"
	array = message.content.split()
	try:
		userid = getUserId(array[1])
	except:
		error = format_exc()
		if "IndexError" in error:
			await message.channel.send(usage)
		else:
			await message.channel.send("""Error while formatting mention into user id.
`"""+error+"`")
			consoleOutput(error)
		return #end command

	try:
		user = await client.get_user_info(userid)
		embed = discord.Embed(title="Avatar for user "+user.name+"#"+user.discriminator)
		embed.set_image(url=user.avatar_url)
		await message.channel.send(embed=embed)
	except:
		error = format_exc()
		if "Unknown User" in error:
			await message.channel.send("No user exists with the ID "+userid)
			consoleOutput("No user exists with the ID "+userid)
		else:
			await message.channel.send("""Unknown error!
`"""+error+"`")
			consoleOutput("""Unknown error!
"""+error)
		return
async def rps(passedvariables):
	#include all the required variables
	message = passedvariables["message"]
	commandprefix = passedvariables["commandprefix"]
	
	usage = "Usage: "+commandprefix+"rps <rock/paper/scissors>"
	array = message.content.split()
	try:
		userchoice = array[1].lower()
	except:
		error = format_exc()
		if "IndexError" in error:
			await message.channel.send(usage)
			
		else:
			await message.channel.send("""Error while reading parameter.
`"""+error+"`")
			consoleOutput(error)
		return #end command

	#cpu choice logic
	cpuchoice = randint(1,3)
	if cpuchoice == 1:
		cpuchoice = "rock"
	elif cpuchoice == 2:
		cpuchoice = "paper"
	else:
		cpuchoice = "scissors"

	#game logic
	#tie
	if cpuchoice == userchoice:
		await message.channel.send("You chose "+userchoice+". I chose "+cpuchoice+". Tie!")
		return
		
	#user wins
	if userchoice == "rock" and cpuchoice == "scissors": result="You won!"
	elif userchoice == "paper" and cpuchoice == "rock": result="You won!"
	elif userchoice == "scissors" and cpuchoice == "paper": result="You won!"

	#cpu wins
	elif cpuchoice == "rock" and userchoice == "scissors": result="You lost!"
	elif cpuchoice == "paper" and userchoice == "rock": result="You lost!"
	elif cpuchoice == "scissors" and userchoice == "paper": result="You lost!"

	#edge case. triggered if user entered invalid string.
	else:
		await message.channel.send("""Invalid option.
"""+usage)
		return

	#send result
	await message.channel.send("You chose "+userchoice+". I chose "+cpuchoice+". "+result)
async def say(passedvariables):
	#include all the required variables
	message = passedvariables["message"]
	commandprefix = passedvariables["commandprefix"]
	
	usage = "Usage: "+commandprefix+"say <text>"
	try:
		#remove command prefix from string we want
		text = message.content[len(commandprefix)+4:] #change according to length of command name + 1 for the space
	except:
		error = format_exc()
		await message.channel.send("""Error while reading text.
`"""+error+"`")
		consoleOutput(error)
		return #end command
	if not text.replace(" ","") == "":
		await message.channel.send(text) #send the message that the user wanted
		await message.delete() #cover their tracks for them
	else:
		await message.channel.send(usage)
async def list_meeps(passedvariables):
	#include all the required variables
	message = passedvariables["message"]
	commandprefix = passedvariables["commandprefix"]
	userData = passedvariables["userData"]
	
	usage = "Usage: "+commandprefix+"list_meeps <mention>"
	array = message.content.split()
	try:
		userid = getUserId(array[1])
	except:
		error = format_exc()
		if "IndexError" in error:
			await message.channel.send(usage)
		else:
			await message.channel.send("""Error while formatting mention into user id.
`"""+error+"`")
			consoleOutput(error)
		return #end command
	value = str(userData.get_user_data(userid,"meeps"))
	await message.channel.send("<@"+userid+"> has meeped "+value+" times.")
async def mca(passedvariables):
	#include all the required variables
	message = passedvariables["message"]
	commandprefix = passedvariables["commandprefix"]
	
	usage = "Usage: "+commandprefix+"mca <text>"
	try:
		#remove command prefix from string we want
		text = message.content[len(commandprefix)+4:] #change according to length of command name + 1 for the space
	except:
		error = format_exc()
		await message.channel.send("""Error while reading text.
`"""+error+"`")
		consoleOutput(error)
		return #end command
	if not text.replace(" ","") == "":
		iconid = randint(1,39)
		response = get('https://www.minecraftskinstealer.com/achievement/a.php?i=%s&h=%s&t=%s' % (iconid, "Achievement get!", text))
		img = Image.open(BytesIO(response.content))

		#unfortunately you cannot send a pillow object using discord.py directly. it must be loaded from a file.
		imageid = str(randint(1,99999999))+".png"  #just to make sure nothing is overwritten in heavy loads.
		img.save(imageid) #save it...
		await message.channel.send(file=discord.File(imageid, filename="img.png")) #then send the image.
		delete_file(imageid) #delete the file afterwards.
	else:
		await message.channel.send(usage)
async def translate(passedvariables):
	#include all the required variables
	message = passedvariables["message"]
	commandprefix = passedvariables["commandprefix"]
	
	usage = "Usage: "+commandprefix+"translate <to/from> <text>"
	#get command parameters and allocate into appropriate variables.
	array = message.content.split()
	try:
		mode = array[1].lower()
	except:
		error = format_exc()
		if "index" in error:
			#in the event that indexing fails (due to no or insufficient parameters), display the usage.
			await message.channel.send("""Missing parameter.
"""+usage)
		else:
			await message.channel.send("""Unknown error while reading array index.
`"""+error+"`")
			consoleOutput(error)
			return #end command

	if "to" not in message.content.lower() and "from" not in message.content.lower(): #check for invalid mode
		await message.channel.send("""Invalid mode.
"""+usage)
		return #end command
	#proper mode selected, lets get separate the text to be translated from the command
	length = len("translate")+2+len(mode) #length of command, 2 for the space, then the length of the mode
	text = message.content[length::].upper() #separate it then capitalize
	if mode == "from":
		await message.channel.send("`"+shadowtranslator.ConvertFromShadow(text)+"`")
	elif mode == "to":
		await message.channel.send("`"+shadowtranslator.ConvertToShadow(text)+"`")
	else:
		#wat.
		#how did you get here??
		raise ExcuseMeWhatTheFuckError("Unexpected error in mode selection")
async def figlet(passedvariables):
	#include all the required variables
	message = passedvariables["message"]
	commandprefix = passedvariables["commandprefix"]
	
	usage = "Usage: "+commandprefix+"figlet <text>"
	
	#find length of input text, then isolate it from the command.
	length = len("figlet")+2 #length of command then 2 for the space
	text = message.content[length::].upper().replace(" ","\n") #separate it then capitalize, then replace spaces with newlines
				
	#check if the input text is empty. if it is, show the usage.
	if text.split() == []:
		await message.channel.send(usage)
		return
				
	try:
		await message.channel.send("```"+pyfiglet.figlet_format(text)+"```")
	except discord.errors.HTTPException:
		await message.channel.send("Message too long.")
async def purge(passedvariables):
	#include all the required variables
	message = passedvariables["message"]
	commandprefix = passedvariables["commandprefix"]
	
	usage = "Usage: "+commandprefix+"purge <number of messages>"
	array = message.content.split()
	try:
		msgcount = int(array[1])
	except:
		error = format_exc()
		if "ValueError" in error:
			await message.channel.send(usage)
		else:
			await message.channel.send("""Unknown error while parsing arguments.
`"""+error+"`")
			consoleOutput(error)
		return #end command
	deletedmsgs = await message.channel.purge(limit=msgcount) #returns a list of information about the deleted messages.
	await message.channel.send("Deleted "+str(len(deletedmsgs))+" messages.")
	
	
	
#image manipulation commands
async def beauty(passedvariables):
	#include all the required variables
	message = passedvariables["message"]
	commandprefix = passedvariables["commandprefix"]
	client = passedvariables["client"]
	core_files_foldername = passedvariables["core_files_foldername"]
	
	usage = "Usage: "+commandprefix+"beauty <mention>"
	array = message.content.split()
	try:
			userid = getUserId(array[1])
	except:
			error = format_exc()
			if "IndexError" in error:
				await message.channel.send(usage)
				return #end command
			else:
				await message.channel.send("""Error while formatting mention into user id.
`"""+error+"`")
				consoleOutput(error)
				return
	background = Image.open(core_files_foldername+"\\images\\beauty.jpg").convert("RGBA") #original meme image

	userdata = await client.get_user_info(userid) #retrieve information of user
	response = get(userdata.avatar_url) #get the image data from the avatar_url and store that into response.
	foreground = Image.open(BytesIO(response.content)).convert("RGBA") #parse response into Image object. This contains the pfp.

	resized = foreground.resize((131,152)) #make foreground the correct size for the target area
	background.paste(resized, (386, 37), resized) #move the foreground into the correct area for the first target area
	resized = foreground.resize((128,154)) #make foreground the correct size for the target area
	background.paste(resized, (389, 338), resized) #move the foreground into the correct area for the second target area

	#unfortunately you cannot send a pillow object using discord.py directly. it must be loaded from a file.
	imageid = str(randint(1,99999999))+".png"  #just to make sure nothing is overwritten in heavy loads.
	background.save(imageid) #save it...
	await message.channel.send(file=discord.File(imageid, filename="img.png")) #then send the image.
	delete_file(imageid) #delete the file afterwards.
async def protecc(passedvariables):
	#include all the required variables
	message = passedvariables["message"]
	commandprefix = passedvariables["commandprefix"]
	client = passedvariables["client"]
	core_files_foldername = passedvariables["core_files_foldername"]
	
	usage = "Usage: "+commandprefix+"protecc <mention>"
	array = message.content.split()
	try:
		userid = getUserId(array[1])
	except:
		error = format_exc()
		if "IndexError" in error:
			await message.channel.send(usage)
			return #end command
		else:
			await message.channel.send("""Error while formatting mention into user id.
`"""+error+"`")
			consoleOutput(error)
			return
	background = Image.open(core_files_foldername+"\\images\\protecc.png").convert("RGBA") #original meme image

	userdata = await client.get_user_info(userid) #retrieve information of user
	response = get(userdata.avatar_url) #get the image data from the avatar_url and store that into response.
	foreground = Image.open(BytesIO(response.content)).convert("RGBA") #parse response into Image object. This contains the pfp.

	foreground = foreground.resize((124,170)).rotate(-24, expand=1) #rotate foreground and make the correct size for the target area
	background.paste(foreground, (382, 129), foreground) #move the foreground into the correct area for the target area

	#unfortunately you cannot send a pillow object using discord.py directly. it must be loaded from a file.
	imageid = str(randint(1,99999999))+".png"  #just to make sure nothing is overwritten in heavy loads.
	background.save(imageid) #save it...
	await message.channel.send(file=discord.File(imageid, filename="img.png")) #then send the image.
	delete_file(imageid) #delete the file afterwards.


#voice channel commands
connectedvoicechannels = {}
async def vc_rickroll(passedvariables):
	#include all the required variables
	message = passedvariables["message"]
	core_files_foldername = passedvariables["core_files_foldername"]

	if message.guild.id in connectedvoicechannels:
		#already playing in another voice channel; disconnect.
		voiceclient = connectedvoicechannels[message.guild.id]
		consoleOutput("Already playing in another voice channel; disconnecting.")
		await voiceclient.disconnect()
		
	if message.author.voice:
		channel = message.author.voice.channel
		consoleOutput("Located channel.")
	else:
		await message.channel.send("You are not in a voice channel.")
		consoleOutput("User is not in channel.")
		return
	
	audio = discord.FFmpegPCMAudio(core_files_foldername+"/audio/rickroll.mp3", executable='ffmpeg') #open file
	audio.volume = 5 #set audio level to 5 out of... something. probably 10.
	consoleOutput("Opened audio file.")
	
	voiceclient = await channel.connect() #connect to the channel
	connectedvoicechannels[message.guild.id] = voiceclient #add the voiceclient to a list for future access.
	consoleOutput("Connected.")
	
	voiceclient.play(audio) #and finally, play the audio file.
	await message.channel.send("Rickrolling.")
	consoleOutput("Rickrolling.")
async def vc_playyt(passedvariables):
	#include all the required variables
	message = passedvariables["message"]
	commandprefix = passedvariables["commandprefix"]

	usage = commandprefix+"play <url/search term>"
	
	if message.guild.id in connectedvoicechannels:
		#already playing in another voice channel; disconnect.
		voiceclient = connectedvoicechannels[message.guild.id]
		consoleOutput("Already playing in another voice channel; disconnecting.")
		await voiceclient.disconnect()
		
	if message.author.voice:
		channel = message.author.voice.channel
		consoleOutput("Located channel.")
	else:
		await message.channel.send("You are not in a voice channel.")
		consoleOutput("User is not in channel.")
		return
	
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
		"retries":"inf", #Number of attempts of connecting to stream before abandoning
		"socket_timeout":3.0 #Number of seconds before giving up on a connection.
	}
	ydl = youtube_dl.YoutubeDL(opts)
	#override information output functions with our custom log function
	ydl.to_stdout = consoleOutput
	ydl.to_stderr = consoleOutput
	try:
		data = str(ydl.extract_info(url, download=False)) #extract metadata from video 
	except:
		#url was not provided; rather a search term.
		data = str(ydl.extract_info("ytsearch:"+url+"\"", download=False)["entries"][0]) #extract metadata from first video result
		
	url = None #reset url variable
	data = literal_eval(data) #parse it
	
	#sift through the barrage of data returned 
	for format in data["formats"]:
		if format["ext"] == "m4a":
			url = format["url"]
			break
	if not url:
		await outputmsg.edit(content=outputmsg.content+"\nUnable to get audio from video.")
		consoleOutput("Unable to get audio version of video. No available formats are M4A.")
		return		
	
	audio = discord.FFmpegPCMAudio(url, executable='ffmpeg') #open stream
	audio.volume = 5 #set audio level to 5 out of... something. probably 10.
	await outputmsg.edit(content=outputmsg.content+"\nOpened audio stream.")
	consoleOutput("Opened audio stream.")
	
	voiceclient = await channel.connect() #connect to the channel
	connectedvoicechannels[message.guild.id] = voiceclient #add the voiceclient to a list for future access.
	await outputmsg.edit(content=outputmsg.content+"\nConnected to voice channel.")
	consoleOutput("Connected to voice channel.")
	
	voiceclient.play(audio) #and finally, play the audio file.
	await outputmsg.edit(content=outputmsg.content+"\nPlaying.")
	consoleOutput("Success.")
async def vc_disconnect(passedvariables):
	message = passedvariables["message"]
	if message.guild.id in connectedvoicechannels:
		#already playing in another voice channel; disconnect.
		voiceclient = connectedvoicechannels[message.guild.id]
		consoleOutput("Disconnecting from voice channel.")
		await voiceclient.disconnect()
		await message.channel.send("Disconnected.")
	else:
		await message.channel.send("I am not in a voice channel on this server.")
		consoleOutput("Bot is not in a voice channel on this server.")



#criminality commands
async def list_crime(passedvariables):
	#include all the required variables
	message = passedvariables["message"]
	commandprefix = passedvariables["commandprefix"]
	userData = passedvariables["userData"]
	
	usage = "Usage: "+commandprefix+"list_crime <mention>"
	array = message.content.split()
	try:
		userid = getUserId(array[1])
	except:
		error = format_exc()
		if "IndexError" in error:
			await message.channel.send(usage)
			return #end command
		else:
			await message.channel.send("""Error while formatting mention into user id.
`"""+error+"`")
			consoleOutput(error)
			return

	if len(array) != 2:
		await message.channel.send(usage)
		return
	value = userData.get_user_data(userid,"criminality")
	await message.channel.send("Criminality value for <@"+userid+"> is "+str(value)+".")
	consoleOutput("Criminality value is now "+str(value)+".")
async def set_crime(passedvariables):
	#include all the required variables
	message = passedvariables["message"]
	commandprefix = passedvariables["commandprefix"]
	userData = passedvariables["userData"]
	
	usage = "Usage: "+commandprefix+"set_crime <mention> <value>"
	array = message.content.split()
	try:
		userid = getUserId(array[1])
	except:
		error = format_exc()
		if "IndexError" in error:
			await message.channel.send(usage)
			return #end command
		else:
			await message.channel.send("""Error while formatting mention into user id.
`"""+error+"`")
			consoleOutput(error)
			return
	if len(array) != 3:
		await message.channel.send(usage)
		return
	value = array[2]
	userData.set_user_data(userid,"criminality",value)
	await message.channel.send("Updated criminality value for <@"+userid+"> to "+str(value)+".")
	consoleOutput("Updated value to "+str(value)+".")
async def change_crime(passedvariables):
	#include all the required variables
	message = passedvariables["message"]
	commandprefix = passedvariables["commandprefix"]
	userData = passedvariables["userData"]
	
	usage = "Usage: "+commandprefix+"change_crime <mention> <value>"
	array = message.content.split()
	try:
		userid = getUserId(array[1])
	except:
		error = format_exc()
		if "IndexError" in error:
			await message.channel.send(usage)
			return #end command
		else:
			await message.channel.send("""Error while formatting mention into user id.
`"""+error+"`")
			consoleOutput(error)
			return

	if len(array) != 3:
		await message.channel.send(usage)
		return

	try:
		prevvalue = int(userData.get_user_data(userid,"criminality"))
	except:
		prevvalue = 0
	try:
		value = int(array[2])
	except:
		value = 0
	finalvalue = prevvalue+value
	userData.set_user_data(userid,"criminality",finalvalue)

	await message.channel.send("Changed criminality value for <@"+userid+"> by "+str(value)+" to equal "+str(finalvalue)+".")
	consoleOutput("Changed criminality value by "+str(value)+" to equal "+str(finalvalue)+".")



#exclusive management commands.
async def shutdown(passedvariables):
	#include all the required variables
	message = passedvariables["message"]
	client = passedvariables["client"]
	
	await message.channel.send("Shutting down bot...")
	await client.change_presence(status=discord.Status.invisible)
	sleep(2)
	force_exit(0)
async def getuserdata(passedvariables):
	#include all the required variables
	message = passedvariables["message"]
	userData = passedvariables["userData"]
	
	array = message.content.split()
	userid = getUserId(array[1])
	await message.channel.send("Access granted.")
	consoleOutput("Access granted.")
	value = str(userData.get_user_data(userid,array[2]))
	await message.channel.send("Value stored with name '"+array[2]+"' for <@"+userid+"> is "+value)
	consoleOutput("Value stored is "+value)
async def setuserdata(passedvariables):
	#include all the required variables
	message = passedvariables["message"]
	userData = passedvariables["userData"]
	
	array = message.content.split()
	userid = getUserId(array[1])
	await message.channel.send("Access granted. Setting user data for <@"+userid+">.")
	consoleOutput("Access granted. Setting user data.")
	userData.set_user_data(userid,array[2],array[3])
	await message.channel.send("Updated value.")
	consoleOutput("Updated value.")
async def execute(passedvariables):
	#include all the required variables
	message = passedvariables["message"]

	await message.channel.send("Access granted. Executing command...")
	consoleOutput("Access granted. Executing command...")
	try:
		cmd = shlex.split(message.content)[1]
	except:
		error = format_exc()
		if "IndexError" in error:
			await message.channel.send(usage)
			return #end command
		else:
			await message.channel.send("""No command was specified.
`"""+error+"`")
			consoleOutput(error)
			return
	output = str(bytes(str(shell_exec(cmd, shell=True, stdout=SUB_PIPE).stdout.read()), "utf-8").decode("unicode_escape"))
	#trim "b'" and "'" from start and end.
	output = output[2:]
	output = output[:-1]
	#send it :D
	await message.channel.send("""```
"""+output+"```")