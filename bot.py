print("Program is now executing.")

#load common functions used in this file
from commands.modules.common import consoleOutput, verifyFolderExistence, generateLogfileName, ExcuseMeWhatTheFuckError

#write newline to log file to separate bot startups.
verifyFolderExistence("logs")
logfile = open(generateLogfileName(),"a")
logfile.write("\n")
logfile.close()
logfile = None

print("Loading vital...")
import discord #This uses the rewrite of the discord module that supports 3.7
import asyncio

print("Loading sub-vital...")
#sub-vital
from traceback import format_exc #for error handling
from commands.modules import database #for all database controls
from time import sleep #bot loop
from time import time as get_unix_epoch #command cooldowns

consoleOutput("Loading commands and their libraries...")
import commands.commands as commands #Load all the commands and their code from the commands.py file

consoleOutput("Modules loaded. Loading configs...")
import commands.modules.config as config

#load configuration files
commandprefix = config.loadConfigFile("bot.config","commandprefix") #sets the command prefix.
core_files_foldername = config.loadConfigFile("bot.config","core_files_foldername") #folder in which the bot looks for its resources
token_filename = config.loadConfigFile("bot.config","api_secret_filename") #file that contains the api token
command_perms = config.loadConfigFile("commands.config") #configuration for specific commands, get the entire thing
admins = config.loadAdmins()

#initialize client and databases
client = discord.Client()
verifyFolderExistence("databases")
userData = database.Database("databases/users.json")

def isAdmin(userid):
	userid = str(userid)
	for entry in admins:
		entry = str(entry)
		if entry == userid:
			return True
	return False

sent_images = {} #initialize dictionary of received images
#Stores command cooldown information
#This is a dictionary of dictionaries, top level is command name to dictionary, second level is user id to unix epoch timestamp
command_cooldowns = {}

@client.event
async def on_ready():
	consoleOutput("Logged on as " + client.user.name + " with the ID " + str(client.user.id) + ".")
	consoleOutput("Bot is in {} guild(s).".format(len(client.guilds)))
	for guild in client.guilds: consoleOutput("\t{}".format(guild.name))
	consoleOutput("------")
	#await client.change_presence(activity=discord.Game(name="DEBUG MODE, BOT NON-FUNCTIONAL"))
	await client.change_presence(activity=discord.Game(name=commandprefix+"help"))

@client.event
async def on_guild_join(guild): #send a message to the first available channel in a new server
	consoleOutput(F"###Joined new server###\nServer name is {guild.name} (#{guild.id}) with {len(guild.members)} members.")
	sent = False
	for channel in guild.channels:
		if not sent:
			try: await channel.send("Hello! I am the Wheatley core. To see what I can do, run the "+commandprefix+"help command.")
			except: continue #Ignore any errors about access denied or whatever, just try the next channel.
		sent = True

@client.event
async def on_guild_remove(guild): #log in console when the bot is removed from a guild
	consoleOutput(F"###Left server###\nServer name is {guild.name} (#{guild.id})")

@client.event
async def on_message(message): #main event that spins off command functions
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

		#define passedvariables dictionary that contains necesscary objects for commmands
		passedvariables = {
			"client":client, #client object
			"message":message, #message object
			"commandprefix":commandprefix, #configured prefix for commands
			"userData":userData, #user information database
			"core_files_foldername":core_files_foldername, #name of the folder that contains bot executables and stuff
			"previous_img":None #last image sent in the channel
		}
		#get the last image sent in the channel from our list for a command to use
		try:
			passedvariables["previous_img"] = sent_images[message.guild.id][message.channel.id]
		except:
			pass #no image to pass to command.

		#log command usage
		if message.content.startswith(commandprefix):
			consoleOutput(author_name + " executed command  " + message.content)
			#start the bot 'typing'. this gives feedback that the bot is calculating the command output.
			await message.channel.trigger_typing() #typing stops either after 10 seconds or when a message is sent.

			#https://stackoverflow.com/questions/35484190/python-if-elif-else-chain-alternitive
			#Kind of like a vector table
			command_set = {
				"help":commands.general.help,
				"test":commands.general.test,
				"dice":commands.general.dice,
				"oxygen":commands.general.oxygen,
				"coin_toss":commands.general.coin_toss,
				"reverse":commands.general.reverse,
				"info":commands.general.info,
				"avatar":commands.general.avatar,
				"rps":commands.general.rps,
				"say":commands.general.say,
				"list_meeps":commands.general.list_meeps,
				"mca":commands.general.mca,
				"translate":commands.general.translate,
				"figlet":commands.general.figlet,
				"wikipedia":commands.general.wikipedia,
				"scp":commands.general.scp_read,

				"beauty":commands.image.beauty,
				"protecc":commands.image.protecc,
				"deepfry":commands.image.deepfry,

				"rickroll":commands.voice.vc_rickroll,
				"play":commands.voice.vc_playyt,
				"s":commands.voice.vc_speak,
				"disconnect":commands.voice.vc_disconnect,

				"list_crime":commands.criminality.list_crime,
				"set_crime":commands.criminality.set_crime,
				"change_crime":commands.criminality.change_crime,

				"shutdown":commands.admin.shutdown,
				"nickname":commands.admin.nickname,
				"purge":commands.general.purge,
				"execute":commands.admin.execute
			}

			if command in command_set and command in command_perms:
				if command_perms[command]["enabled"]: #verify the command is enabled via the config
					if command_perms[command]["adminsonly"]: #then check if only admins can use it
						#permission check
						if not isAdmin(message.author.id):
							await message.channel.send("Access denied.")
							consoleOutput("Access denied.")
							return
				else:
					await message.channel.send("This command has been disabled.")
					consoleOutput("Command has been disabled.")
					return

				#check if the command is in a cooldown state for that user
				if command in command_cooldowns.keys(): #check if that specific command has any users on cooldown
					if message.author.id in command_cooldowns[command].keys(): #now check if the message author is in that list
						#they are. check if their cooldown period has ended.
						time_remaining = command_perms[command]["cooldown"] - (int(get_unix_epoch()) - command_cooldowns[command][message.author.id])
						if time_remaining > 0:
							consoleOutput(F"User is blocked from that command for {time_remaining} seconds.")
							await message.channel.send(F"You need to wait {time_remaining} seconds before you can do that again.")
							return
						else:
							#remove the entry since their cooldown has expired
							command_cooldowns[command].pop(message.author.id)

				#The user is allowed to execute the command and it is not disabled.
				#lookup the command being referenced
				action = command_set[command]

				#finally, execute the command.
				await action(passedvariables)

				#now we need to add a cooldown period for that command for that user if applicable
				if command_perms[command]["cooldown"] > 0:
					consoleOutput("Cooldown in effect for that user.")
					if command not in command_cooldowns.keys(): command_cooldowns[command] = {}
					command_cooldowns[command][message.author.id] = int(get_unix_epoch())
			else:
				#if the command does not have a function to run (because it isnt in command_set) OR its entry is omitted from the config, report unknown command.
				await message.channel.send("Unknown command '"+command+"'.")

		#spin off function to check for phrases to react to autonomously
		await commands.react_phrases.main(passedvariables)
	except:
		error = format_exc()
		await message.channel.send("""Internal error while running command! Error traceback:
`"""+error+"`")
		consoleOutput(error)


#while True: print(eval(input("BOT> ")))


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
			continue
