print("Program is now executing.")

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
def consoleOutput(text): #consoleOutput is encouraged as a replacement of print as it writes everything to a log file.
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

#write newline to log file to separate bot startups.
logfile = open(logfilename,"a")
logfile.write("\n")
logfile.close()
logfile = None

print("Loading vital...")
import discord #This uses the rewrite of the discord module that supports 3.7
import asyncio

print("Loading sub-vital...")
#sub-vital
from traceback import format_exc #for error handling
from modules import database #for all database controls
import json #for parsing command permission configs

consoleOutput("Loading commands and their libraries...")
import commands #Load all the commands and their code from the commands.py file
from time import sleep #bot loop

consoleOutput("Modules loaded. Loading configs...")

#get ids of bot admins from admins.config.
#used for exclusive management commands and access denied reporting.
#custom error class for comedic purposes in hilariously catastrophic scenarios
class EmptyConfigFileError(Exception):
    pass
class ConfigFileError(Exception):
    pass
class ConfigLoader():
	def loadGeneralConfig(key):
		try:
			with open('bot.config') as json_data:
				config = json.load(json_data)
				return config[key]
		except:
			raise ConfigFileError("Unable to open bot.config")
	def loadAdmins():
		admins = []
		try:
			for line in open("admins.config").readlines():
				line = line.replace("\n","")
				if line.split() == [] or line.startswith("#"):
					continue
				else:
					admins.append(line)
			if len(admins) == 0:
				raise EmptyConfigFileError("ERROR! No admins are defined in admins.config! Aborting...")
			return admins
		except:
			raise ConfigFileError("Unable to open admins.config")
	def loadCommandPerms():
		try:
			with open('commands.config') as json_data:
				config = json.load(json_data)
				return config
		except:
			raise ConfigFileError("Unable to open commands.config")

async def reloadConfigs(passedvariables):
	#include all the required variables
	message = passedvariables["message"]
	global core_files_foldername
	global admins
	global command_perms
	global token_filename

	try:
		commandprefix = ConfigLoader.loadGeneralConfig("commandprefix")
		core_files_foldername = ConfigLoader.loadGeneralConfig("core_files_foldername")
		token_filename = ConfigLoader.loadGeneralConfig("api_secret_filename")
	except:
		error = format_exc()
		if "FileNotFound" in error:
			await message.channel.send("ERROR! 'bot.config' is missing.")
			consoleOutput("ERROR! 'bot.config' is missing.")

	try:
		admins = ConfigLoader.loadAdmins()
	except:
		error = format_exc()
		if "FileNotFound" in error:
			await message.channel.send("ERROR! 'admins.config' is missing.")
			consoleOutput("ERROR! 'admins.config' is missing.")
	try:
		command_perms = ConfigLoader.loadCommandPerms()
	except:
		error = format_exc()
		if "FileNotFound" in error:
			await message.channel.send("ERROR! 'commands.config' is missing.")
			consoleOutput("ERROR! 'commands.config' is missing.")

	await message.channel.send("Reloaded configuration files.")
	consoleOutput("Reloaded configuration files.")

commandprefix = ConfigLoader.loadGeneralConfig("commandprefix") #sets the command prefix.
core_files_foldername = ConfigLoader.loadGeneralConfig("core_files_foldername") #folder in which the bot looks for its resources
token_filename = ConfigLoader.loadGeneralConfig("api_secret_filename") #file that contains the api token
admins = ConfigLoader.loadAdmins()
command_perms = ConfigLoader.loadCommandPerms()

#initialize client and databases
client = discord.Client()
verifyFolderExistence("databases")
userData = database.Database("databases\\users.json")

#Load opus library. Needed for voice channel support
try:
	discord.opus.load_opus(core_files_foldername+"\\libopus-0.x86.dll")
except:
	error = format_exc()
	consoleOutput("!!ERROR LOADING OPUS LIBRARY!!")
	consoleOutput("Commands that utilise voice channels will not work.")

#custom error class for comedic purposes in hilariously catastrophic scenarios
class ExcuseMeWhatTheFuckError(Exception):
    pass

def isAdmin(userid):
	userid = str(userid)
	for entry in admins:
		entry = str(entry)
		if entry == userid:
			return True
	return False

sent_images = {} #initialize dictionary of received images

@client.event
async def on_ready():
	consoleOutput("Logged on as " + client.user.name + " with the ID " + str(client.user.id) + ".")
	consoleOutput("------")
	#await client.change_presence(activity=discord.Game(name="DEBUG MODE, BOT NON-FUNCTIONAL"))
	await client.change_presence(activity=discord.Game(name=commandprefix+"help"))

@client.event
async def on_message(message):
	try:
		#check if the message was sent by the bot. if so, drop it to ensure infinite loops of command execution cannot occur.
		if client.user.id == message.author.id:
			return

		#convert any unicode in author name to ascii. quick and dirty way to prevent codec errors
		author_name = message.author.name.encode('ascii','ignore').decode('ascii','ignore')

		#if the message contains an image, keep track of it so a command can use it.
		if len(message.attachments) >= 1: #check for attachment
			if message.attachments[0].width: #detect if an image was sent by measuring the width of the image.
				if not message.guild.id in sent_images.keys(): #check if the server doesn't already exist in our list
					sent_images[message.guild.id] = {} #the sub-dictionary for different channels within a server.
				sent_images[message.guild.id][message.channel.id] = message.attachments[0] #add the image to the list.

		try:
			command = message.content.lower().split()[0][len(commandprefix):]
		except:
			#bot joins / emoji throws an exception because we use ASCII, so this ignores messages that contain unhandleable characters.
			return

		#log command usage
		if message.content.startswith(commandprefix):
			consoleOutput(author_name + " executed command  " + message.content)
			#start the bot 'typing'. this gives feedback that the bot is calculating the command output.
			await message.channel.trigger_typing() #typing stops either after 10 seconds or when a message is sent.

			#https://stackoverflow.com/questions/35484190/python-if-elif-else-chain-alternitive
			command_set = {
				"help":commands.help,
				"test":commands.test,
				"dice":commands.dice,
				"oxygen":commands.oxygen,
				"coin_toss":commands.coin_toss,
				"reverse":commands.reverse,
				"info":commands.info,
				"avatar":commands.avatar,
				"rps":commands.rps,
				"say":commands.say,
				"list_meeps":commands.list_meeps,
				"mca":commands.mca,
				"translate":commands.translate,
				"figlet":commands.figlet,
				"wikipedia":commands.wikipedia,
				"purge":commands.purge,

				"beauty":commands.beauty,
				"protecc":commands.protecc,
				"deepfry":commands.deepfry,

				"rickroll":commands.vc_rickroll,
				"play":commands.vc_playyt,
				"disconnect":commands.vc_disconnect,

				"list_crime":commands.list_crime,
				"set_crime":commands.set_crime,
				"change_crime":commands.change_crime,

				"shutdown":commands.shutdown,
				"getuserdata":commands.getuserdata,
				"setuserdata":commands.setuserdata,
				"execute":commands.execute,
				"reload":reloadConfigs
			}

			if command in command_set and command in command_perms:
				can_do_command = True
				if command_perms[command]["enabled"]:
					if command_perms[command]["adminsonly"]:
						#permission check
						if not isAdmin(message.author.id):
							can_do_command = False
							await message.channel.send("Access denied.")
							consoleOutput("Access denied.")
				else:
					can_do_command = False
					await message.channel.send("This command has been disabled.")
					consoleOutput("Command has been disabled.")

				if can_do_command:
					#find the command being referenced
					action = command_set[command]

					#get the last image sent in the channel from our list for a command to use
					try:
						previous_img = sent_images[message.guild.id][message.channel.id]
					except:
						previous_img = None #no image to pass to command.

					#define passedvariables (dictionary that contains additional objects)
					passedvariables = {
						"client":client, #client object
						"message":message, #message object
						"commandprefix":commandprefix, #configured prefix for commands
						"userData":userData, #user information database
						"core_files_foldername":core_files_foldername, #name of the folder that contains bot executables and stuff
						"previous_img":previous_img #last image sent in the channel
					}
					#execute the command
					await action(passedvariables)
			else:
				#if none of the above worked, report unknown command.
				await message.channel.send("Unknown command '"+command+"'.")

		#triggerwords
		if "meep" in message.content.lower() and "list_" not in message.content.lower(): #prevents >list_meeps from triggering.
				await message.channel.send("Meep")
				userData.set_user_data(message.author.id,"meeps",int(userData.get_user_data(message.author.id,"meeps"))+1)
		if "wheatley"  in message.content.lower() and "moron" in message.content.lower(): #message must have the words "wheatley" and "moron" to trigger.
				await message.channel.send("I AM NOT A MORON!")
		if "pineapple" in message.content.lower():
				await message.channel.send("""```
Pine
Independance
Never
Ends
Attacks
People
Providing
Little
Economy
```""")
		if "no u" in message.content.lower() or "no you" in message.content.lower():
				await message.channel.send(file=discord.File(core_files_foldername+"\\images\\no_u.jpg", filename="img.png"))
		if "the more you know" in message.content.lower():
				await message.channel.send(file=discord.File(core_files_foldername+"\\images\\moreyouknow.gif", filename="img.png"))

	except:
		error = format_exc()
		await message.channel.send("""Internal error while running command! Error traceback:
`"""+error+"`")
		consoleOutput(error)

try:
	tokenfile = open(token_filename,"r")
except:
	consoleOutput("API token file ("+token_filename+") is missing.")
	exit()

#get the bot token from the external file
for line in tokenfile.readlines():
	if not line.startswith("#") or line.split() == []: #ignores comments and blank lines in the token file
		token = line.rstrip()
if not len(token): #check if there was a gleanable token from the file. if not, raise an error.
	raise ExcuseMeWhatTheFuckError("No token found in api_secret.token")

#run the bot
consoleOutput("Logging on...")
loop = asyncio.get_event_loop()
while True:
	try:
		loop.run_until_complete(client.start(token))
	except:
		error = format_exc()
		if "Improper token" in error:
			consoleOutput("Configured token is invalid!")
			break #exit restart loop since it will never startup.
		elif "KeyboardInterrupt" in error: #killing the bot via ^C results in KeyboardInterrupts.
			consoleOutput("KeyboardInterrupt detected: Forcibly shutting down bot.")
			break #exit loop since we have aborted the loop.
		else:
			#error while connecting to discord. reconnect after waiting for 5 seconds.
			consoleOutput(error)
			consoleOutput("Waiting 10 seconds then restarting bot...")
			sleep(10)

			#following "The Great Disconnect" (the Pi disconnected from WiFi and filled the disk with 18GB of errors),
			#it now store logs in separate files. on bot restarts, we should re-evaluate which log file to write to.
			time = localtime() #get the time
			logfilename = "logs\\log_"+str(time[0])+"-"+str(time[1])+"-"+str(time[2])+".txt" #determine which log file we should write to based on the date
			continue
