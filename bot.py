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

consoleOutput("Loading commands and their libraries...")
import commands.commands as commands #Load all the commands and their code from the commands.py file
from time import sleep #bot loop

consoleOutput("Modules loaded. Loading configs...")
import commands.modules.config as config

#load configuration files
commandprefix = config.loadGeneralConfig("commandprefix") #sets the command prefix.
core_files_foldername = config.loadGeneralConfig("core_files_foldername") #folder in which the bot looks for its resources
token_filename = config.loadGeneralConfig("api_secret_filename") #file that contains the api token
wolfram_alpha_token = config.loadGeneralConfig("wolfram_alpha_token") #file that contains the api token for wolfram alpha
admins = config.loadAdmins()
command_perms = config.loadCommandPerms()

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
def isWholeWordInString(sentence,searchterm):
	searchterms = searchterm.split()
	found = True
	#https://cmsdk.com/python/checking-if-a-whole-word-is-in-a-text-file-in-python-without-regex.html
	sentence = ''.join(char for char in sentence if char.isalpha() or char.isspace()).split()
	for searchterm in searchterms:
		if not searchterm in sentence:
			found = False
			break
	return found

sent_images = {} #initialize dictionary of received images
voiceclients = {} #list of active voice clients to be referenced by commands.

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
				"purge":commands.general.purge,
				"scp":commands.general.scp_read,
				"math":commands.general.math_solve,

				"beauty":commands.image.beauty,
				"protecc":commands.image.protecc,
				"deepfry":commands.image.deepfry,

				"rickroll":commands.voice.vc_rickroll,
				"play":commands.voice.vc_playyt,
				"speak":commands.voice.vc_speak,
				"disconnect":commands.voice.vc_disconnect,

				"list_crime":commands.criminality.list_crime,
				"set_crime":commands.criminality.set_crime,
				"change_crime":commands.criminality.change_crime,

				"shutdown":commands.admin.shutdown,
				"execute":commands.admin.execute
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
						"wolfram_alpha_token":wolfram_alpha_token, #api token for wolfram alpha
						"previous_img":previous_img, #last image sent in the channel
						"connectedvoicechannels":voiceclients
					}
					#execute the command
					await action(passedvariables)
			else:
				#if none of the above worked, report unknown command.
				await message.channel.send("Unknown command '"+command+"'.")

		#triggerwords
		msg_lowercase = message.content.lower()
		if isWholeWordInString(msg_lowercase, "meep"):
			await message.channel.send("Meep")
			userData.set_user_data(message.author.id,"meeps",int(userData.get_user_data(message.author.id,"meeps"))+1)
		if isWholeWordInString(msg_lowercase, "wheatley") and isWholeWordInString(msg_lowercase, "moron"): #message must have the words "wheatley" and "moron" to trigger.
				await message.channel.send("I AM NOT A MORON!")
		if isWholeWordInString(msg_lowercase, "pineapple"):
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
		if isWholeWordInString(msg_lowercase, "no u") or isWholeWordInString(msg_lowercase, "no you"):
				await message.channel.send(file=discord.File(core_files_foldername+"/images/no_u.jpg", filename="img.png"))
		if isWholeWordInString(msg_lowercase, "the more you know"):
				await message.channel.send(file=discord.File(core_files_foldername+"/images/moreyouknow.gif", filename="img.png"))

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
