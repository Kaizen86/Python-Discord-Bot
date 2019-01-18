print("Program is now executing.")
lengthofthisfile = 766

from time import localtime #file logs, shutdown
from os import listdir #help, folder existence checks
from os import mkdir #make new folder if needed

def verifyFolderExistence(foldername):
	if foldername not in listdir():
		print("Making '"+foldername+"' folder.")
		mkdir(foldername)
		
time = localtime() #get the time
verifyFolderExistence("logs")
logfilename = "logs\\log_"+str(time[0])+"-"+str(time[1])+"-"+str(time[2])+".txt" #determine which log file we should write to based on the date
def consoleOutput(text): #consoleOutput is encouraged as a replacement of print as it writes everything to a log file.
	#consoleOutputs to the console
	print(text)
	#get time and date
	time = localtime()
	#format text to have timestamp
	text = str(time[0])+"/"+str(time[1])+"/"+str(time[2])+" "+str(time[3])+":"+str(time[4])+":"+str(time[5])+": "+text
	#write to log
	logfile = open(logfilename,"a")
	logfile.write(text+"\n")
	logfile.close()

#write newline to log file to separate bot startups.
logfile = open(logfilename,"a")
logfile.write("\n")
logfile.close()
logfile = None

consoleOutput("Loading libraries...")
print("\tLoading vital...")
#vital
import discord
import asyncio

print("\tLoading sub-vital...")
#sub-vital
from traceback import format_exc #for error handling
from modules import database #for all database controls

print("\tLoading command dependencies...")
#used by commands (carefully sorted alphabetically :))
from io import BytesIO #mca, beauty, protecc
from modules import shadow_translator #translate

from os import remove as delete_file #mca, beauty, protecc
from os import _exit as force_exit #shutdown
from PIL import Image #mca, beauty, protecc
from random import randint #dice, coin_toss, rps, mca, beauty, protecc
import re #used to remove non-numbers from mentions to extract the user id
from requests import get #mca, beauty, protecc
from subprocess import PIPE as SUB_PIPE #exec
from subprocess import Popen as shell_exec #exec
from sys import version_info as python_info #help
from time import sleep #shutdown, bot loop
import pyfiglet #figlet

consoleOutput("Modules loaded. Loading configs and command set...")
commandprefix = ">" #sets the command prefix.

#get ids of bot admins from admins.config. 
#used for exclusive management commands and access denied reporting.
admins = []
try:
	for line in open("admins.config").readlines():
		line = line.replace("\n","")
		if line.split() == [] or line.startswith("#"):
			continue
		else:
			admins.append(line)
	if len(admins) == 0:
		consoleOutput("ERROR! No admins are defined in admin.config! Aborting...")
		exit()
except:
	error = format_exc()
	if "FileNotFound" in error:
		consoleOutput("ERROR! 'admins.config' is missing. Aborting...")
		exit()

#initialize client, databases and shadow_translator
client = discord.Client()
userData = database.Database("databases\\users.json")
shadowtranslator = shadow_translator.ShadowTranslator()

#custom error class for comedic purposes in hilariously catastrophic scenarios
class ExcuseMeWhatTheFuckError(Exception):
    pass
	
def isAdmin(userid):
	for entry in admins:
		if entry ==  userid:
			return True
	return False
async def reportAccessDenied(message):
	#in the event that someone attempts to access a management command,
	#send a direct message to the owner and warn the offending user.

	#construct the embedded message
	embed = discord.Embed(title="User attempted unauthorised access!")
	embed.add_field(name="Offending message content", value=message.content, inline=False)
	embed.add_field(name="Username", value=message.author.name+"#"+str(message.author.discriminator), inline=False)
	embed.add_field(name="Unique ID", value=message.author.id, inline=False)
	embed.add_field(name="Avatar", value=" ", inline=False)
	embed.set_image(url=message.author.avatar_url)

	botownermember = discord.Server.get_member(message.server, admins[0]) #create a new user object and point it at the bot owner
	if botownermember != None:
		try:
			await client.send_message(botownermember,embed=embed) #send it. this fails if content is over 2000 chars.
		finally:
			await client.send_message(message.channel, "Access denied. This incident has been reported.")
	else:
		await client.send_message(message.channel, "Access denied.")

@client.event
async def on_ready():
	consoleOutput("Logged on as " + client.user.name + " with the ID " + client.user.id + ".")
	consoleOutput("------")
	await client.change_presence(game=discord.Game(name=commandprefix+"help"))
	while True:
		command = input(">").split()
		
@client.event
async def on_message(message):
	try:
		#check if the message was sent by the bot. if so, drop it to ensure infinite loops of command execution cannot occur.
		if client.user.id == message.author.id:
			return

		#convert any unicode to ascii. quick and dirty way to prevent codec errors
		author_name = message.author.name.encode('ascii','ignore').decode('ascii','ignore')
		message_content = message.content.encode('ascii','ignore').decode('ascii','ignore')

		try:
			command = message_content.lower().split()[0]
		except:
			#bot joins / emoji throws an exception, so this ignores that.
			return

		#log command usage
		if command.startswith(commandprefix):
			consoleOutput(author_name + " executed command  " + message_content)
			#start the bot 'typing'. this gives feedback that the bot is calculating the command output.
			await client.send_typing(message.channel) #typing stops either after 10 seconds or when a message is sent.

		#user commands
		if command == commandprefix+"help":
			"""
			#get number of lines of code in this script and all scripts in the 'modules' folder.
			#this file
			with open("bot.py") as f:
				linecount = len(f.readlines())
			"""
			linecount = lengthofthisfile
			#everything in modules
			for scriptname in listdir("modules"):
				try:
					with open("modules\\"+scriptname) as f:
						linecount += len(f.readlines())
				except Exception:
					continue #ignore errors if a folder was selected
			#send help message to dm of user
			await client.send_message(message.author, """(User Commands)
```
These commands are accessible to all users.
Display this help.
	"""+commandprefix+"""help
Tests if the bot is working.
	"""+commandprefix+"""test
Rolls a dice with an optional minimum and maximum limits
	"""+commandprefix+"""dice [minimum [maximum]
Gives advice on where to find oxygen. In other words, the perfect command.
	"""+commandprefix+"""oxygen
Tosses a coin. That's it.
	"""+commandprefix+"""coin_toss
Reverses the given text
	"""+commandprefix+"""reverse <text>
Gets information about a mentioned user
	"""+commandprefix+"""info <mention>
Gets the avatar of a mentioned user
	"""+commandprefix+"""avatar <mention>
Play a game of rock paper scissors with the bot. (I promise it doesn't cheat)
	"""+commandprefix+"""rps <rock/paper/scissors>
Gets the bot to repeat the input text. The bot will then try and delete your message to make it look real.
	"""+commandprefix+"""say <text>
Gets the number of times the mentioned user has "meeped".
	"""+commandprefix+"""list_meeps <mention>
This command allow translation to and from Basic Shadow, which is a language invented by <@284415695050244106>.
	"""+commandprefix+"""translate <to/from> <english>
```

Image manipulation commands
```
	"""+commandprefix+"""beauty <mention>
	"""+commandprefix+"""protecc <mention>
```

Criminality Commands
```
These commands control or list the criminality values of a user.
	"""+commandprefix+"""list_crime <mention>
	"""+commandprefix+"""set_crime <mention> <value>
	"""+commandprefix+"""change_crime <mention> <increment value by>
```

Trigger Words
```
These are words that have make the bot do something if you say them.

	"meep"
	"wheatley" AND "moron"
	"pineapple"
	"no u" or "no you"
	"the more you know"
```

(Bot Administration Commands)
```
These commands are strictly for the bot owners. Accessing them will send a warning to the owner.

Shutdown the bot.
	"""+commandprefix+"""shutdown
Retrieve stored value for user attribute in database
	"""+commandprefix+"""getuserdata <mention> <attribute>
Update stored value for user attribute in database
	"""+commandprefix+"""setuserdata <mention> <attribute> <value>
Execute a shell command on the host computer
	"""+commandprefix+"""exec <shell command>

	"""+commandprefix+"""nuke <message count>
```
Created with `"""+str(linecount)+"""` lines of Python written by <@285465719292821506>.
Python version is """+str(python_info.major)+"."+str(python_info.minor)+".")
			await client.send_message(message.channel, "List of commands sent in DM.")
		elif command == commandprefix+"test":
			await client.send_message(message.channel, "Yes, <@"+message.author.id+">, This bot is online.")
		elif command.startswith(commandprefix+"dice"):
			usage = "Usage: "+commandprefix+"dice [minimum] [maximum]"
			#get command parameters and allocate into appropriate variables.
			array = message_content.split()
			if len(array) > 1:
				try:
					min = int(array[1])
					max = int(array[2])
				except:
					error = format_exc()
					if "index" in error:
						#in the event that indexing fails (due to no or insufficient parameters, display the usage.
						await client.send_message(message.channel, usage)
					elif "invalid literal" in error:
						#in the event that conversion to an integer fails (likely due to text being entered instead of numbers), display this.
						await client.send_message(message.channel, """Minimum and maximum values must be numbers.
"""+usage)
					else:
						await client.send_message(message.channel, """Unknown error while reading array index.
`"""+error+"`")
						consoleOutput(error)
					return #end command
			else:
				#no parameters were specified, so the defaults are a regular die.
				min = 1
				max = 6

			if min<max:
				#roll the dice
				await client.send_message(message.channel, "I rolled "+str(randint(min,max)))
			else:
				await client.send_message(message.channel, "Minimum & maximum must be numbers.")
		elif command == commandprefix+"oxygen":
			await client.send_message(message.channel, "Look around and you will find it.")
		elif command == commandprefix+"coin_toss":
			result = randint(1,8)
			if result <= 4:
				result = "Tails"
			else:
				result = "Heads"
			await client.send_message(message.channel, result+".")
		elif command.startswith(commandprefix+"reverse"):
			usage = "Usage: "+commandprefix+"reverse <text>"
			try:
				#remove command prefix from string we want
				text = message_content[len(commandprefix)+8:] #change according to length of command name + 1 for the space
			except:
				error = format_exc()
				await client.send_message(message.channel, """Error while reading text.
`"""+error+"`")
				consoleOutput(error)
				return #end command
			if not text.replace(" ","") == "":
				await client.send_message(message.channel, text[::-1]) #mystical string manipulation command to reverse the input
			else:
				await client.send_message(message.channel, usage)
		elif command.startswith(commandprefix+"info"):
			usage = "Usage: "+commandprefix+"info <mention>"
			array = message_content.split()
			try:
				userid = re.sub("[^0-9]","",array[1])
			except:
				error = format_exc()
				if "IndexError" in error:
					await client.send_message(message.channel, usage)
				else:
					await client.send_message(message.channel, """Error while formatting mention into user id.
`"""+error+"`")
					consoleOutput(error)
				return #end command

			try:
				user = await client.get_user_info(userid)
			except:
				error = format_exc()
				if "Unknown User" in error:
					await client.send_message(message.channel,"No user exists with the ID "+userid)
					consoleOutput("No user exists with the ID "+userid)
					return
			embed = discord.Embed(title="Data dump for user "+user.name+"#"+user.discriminator)
			embed.add_field(name="Is a bot", value=user.bot, inline=False)
			embed.add_field(name="Date created", value=user.created_at, inline=False)
			embed.add_field(name="Nickname", value=user.display_name, inline=False)
			embed.add_field(name="Unique ID", value=user.id, inline=False)
			embed.add_field(name="Avatar", value=".", inline=False)
			embed.set_image(url=user.avatar_url)
			await client.send_message(message.channel,embed=embed)
		elif command.startswith(commandprefix+"avatar"):
			usage = "Usage: "+commandprefix+"avatar <mention>"
			array = message_content.split()
			try:
				userid = re.sub("[^0-9]","",array[1])
			except:
				error = format_exc()
				if "IndexError" in error:
					await client.send_message(message.channel, usage)
				else:
					await client.send_message(message.channel, """Error while formatting mention into user id.
`"""+error+"`")
					consoleOutput(error)
				return #end command

			try:
				user = await client.get_user_info(userid)
				embed = discord.Embed(title="Avatar for user "+user.name+"#"+user.discriminator)
				embed.set_image(url=user.avatar_url)
				await client.send_message(message.channel,embed=embed)
			except:
				error = format_exc()
				if "Unknown User" in error:
					await client.send_message(message.channel,"No user exists with the ID "+userid)
					consoleOutput("No user exists with the ID "+userid)
				else:
					await client.send_message(message.channel,"""Unknown error!
`"""+error+"`")
					consoleOutput("""Unknown error!
"""+error)
				return
		elif command.startswith(commandprefix+"rps"):
			usage = "Usage: "+commandprefix+"rps <rock/paper/scissors>"
			array = message_content.split()
			try:
				userchoice = array[1].lower()
			except:
				error = format_exc()
				if "IndexError" in error:
					await client.send_message(message.channel, usage)
					
				else:
					await client.send_message(message.channel, """Error while reading parameter.
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
				await client.send_message(message.channel, "You chose "+userchoice+". I chose "+cpuchoice+". Tie!")
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
				await client.send_message(message.channel, """Invalid option.
"""+usage)
				return

			#send result
			await client.send_message(message.channel, "You chose "+userchoice+". I chose "+cpuchoice+". "+result)
		elif command.startswith(commandprefix+"say"):
			usage = "Usage: "+commandprefix+"say <text>"
			try:
				#remove command prefix from string we want
				text = message.content[len(commandprefix)+4:] #change according to length of command name + 1 for the space
			except:
				error = format_exc()
				await client.send_message(message.channel, """Error while reading text.
`"""+error+"`")
				consoleOutput(error)
				return #end command
			if not text.replace(" ","") == "":
				await client.send_message(message.channel, text) #send the message that the user wanted
				await client.delete_message(message) #cover their tracks for them
			else:
				await client.send_message(message.channel, usage)
		elif command.startswith(commandprefix+"list_meeps"):
			usage = "Usage: "+commandprefix+"list_meeps <mention>"
			array = message_content.split()
			try:
				userid = re.sub("[^0-9]","",array[1])
			except:
				error = format_exc()
				if "IndexError" in error:
					await client.send_message(message.channel, usage)
				else:
					await client.send_message(message.channel, """Error while formatting mention into user id.
`"""+error+"`")
					consoleOutput(error)
				return #end command
			value = str(userData.get_user_data(userid,"meeps"))
			await client.send_message(message.channel, "<@"+userid+"> has meeped "+value+" times.")
		elif command.startswith(commandprefix+"mca"):
			usage = "Usage: "+commandprefix+"mca <text>"
			try:
				#remove command prefix from string we want
				text = message_content[len(commandprefix)+4:] #change according to length of command name + 1 for the space
			except:
				error = format_exc()
				await client.send_message(message.channel, """Error while reading text.
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
				await client.send_file(message.channel, imageid) #then send the image.
				delete_file(imageid) #delete the file afterwards.
			else:
				await client.send_message(message.channel, usage)
		elif command.startswith(commandprefix+"translate"):
			usage = "Usage: "+commandprefix+"translate <to/from> <text>"
			#get command parameters and allocate into appropriate variables.
			array = message_content.split()
			try:
				mode = array[1].lower()
			except:
				error = format_exc()
				if "index" in error:
					#in the event that indexing fails (due to no or insufficient parameters), display the usage.
					await client.send_message(message.channel, """Missing parameter.
"""+usage)
				else:
					await client.send_message(message.channel, """Unknown error while reading array index.
`"""+error+"`")
					consoleOutput(error)
					return #end command

				if "to" not in message_content.lower() and "from" not in message_content.lower(): #check for invalid mode
					await client.send_message(message.channel, """Invalid mode.
"""+usage)
					return #end command
				#proper mode selected, lets get separate the text to be translated from the command
				length = len("translate")+2+len(mode) #length of command, 2 for the space, then the length of the mode
				text = message_content[length::].upper() #separate it then capitalize
				if mode == "from":
					await client.send_message(message.channel, "`"+shadowtranslator.ConvertFromShadow(text)+"`")
				elif mode == "to":
					await client.send_message(message.channel, "`"+shadowtranslator.ConvertToShadow(text)+"`")
				else:
					#wat.
					#how did you get here??
					raise ExcuseMeWhatTheFuckError("Unexpected error in mode selection")
		elif command.startswith(commandprefix+"figlet"):
						usage = "Usage: "+commandprefix+"figlet <text>"
						
						#find length of input text, then isolate it from the command.
						length = len("figlet")+2 #length of command then 2 for the space
						text = message_content[length::].upper().replace(" ","\n") #separate it then capitalize, then replace spaces with newlines
						
						#check if the input text is empty. if it is, show the usage.
						if text.split() == []:
							await client.send_message(message.channel, usage)
							return
						
						try:
							await client.send_message(message.channel, "```"+pyfiglet.figlet_format(text)+"```")
						except discord.errors.HTTPException:
							await client.send_message(message.channel, "Message too long.")
						
		#image manipulation commands
		elif command.startswith(commandprefix+"beauty"):
						usage = "Usage: "+commandprefix+"beauty <mention>"
						array = message_content.split()
						try:
								userid = re.sub("[^0-9]","",array[1])
						except:
								error = format_exc()
								if "IndexError" in error:
										await client.send_message(message.channel, usage)
										return #end command
								else:
										await client.send_message(message.channel, """Error while formatting mention into user id.
`"""+error+"`")
										consoleOutput(error)
										return
						background = Image.open("images\\beauty.jpg").convert("RGBA") #original meme image

						userdata = await client.get_user_info(userid) #retrieve information of user
						response = get(userdata.avatar_url) #get the image data from the avatar_url and store that into response.
						foreground = Image.open(BytesIO(response.content)).convert("RGBA") #parse response into Image object. This contains the pfp.

						foreground = foreground.resize((150,175)) #make foreground the correct size for the target area
						background.paste(foreground, (437, 38), foreground) #move the foreground into the correct area for the first target area
						background.paste(foreground, (440, 380), foreground) #move the foreground into the correct area for the second target area

						#unfortunately you cannot send a pillow object using discord.py directly. it must be loaded from a file.
						imageid = str(randint(1,99999999))+".png"  #just to make sure nothing is overwritten in heavy loads.
						background.save(imageid) #save it...
						await client.send_file(message.channel, imageid) #then send the image.
						delete_file(imageid) #delete the file afterwards.
		elif command.startswith(commandprefix+"protecc"):
						usage = "Usage: "+commandprefix+"protecc <mention>"
						array = message_content.split()
						try:
								userid = re.sub("[^0-9]","",array[1])
						except:
								error = format_exc()
								if "IndexError" in error:
										await client.send_message(message.channel, usage)
										return #end command
								else:
										await client.send_message(message.channel, """Error while formatting mention into user id.
`"""+error+"`")
										consoleOutput(error)
										return
						background = Image.open("images\\protecc.png").convert("RGBA") #original meme image

						userdata = await client.get_user_info(userid) #retrieve information of user
						response = get(userdata.avatar_url) #get the image data from the avatar_url and store that into response.
						foreground = Image.open(BytesIO(response.content)).convert("RGBA") #parse response into Image object. This contains the pfp.

						foreground = foreground.resize((124,170)).rotate(-24, expand=1) #rotate foreground and make the correct size for the target area
						background.paste(foreground, (391, 131), foreground) #move the foreground into the correct area for the target area

						#unfortunately you cannot send a pillow object using discord.py directly. it must be loaded from a file.
						imageid = str(randint(1,99999999))+".png"  #just to make sure nothing is overwritten in heavy loads.
						background.save(imageid) #save it...
						await client.send_file(message.channel, imageid) #then send the image.
						delete_file(imageid) #delete the file afterwards.

		#criminality commands
		elif command.startswith(commandprefix+"list_crime"):
						usage = "Usage: "+commandprefix+"list_crime <mention>"
						array = message_content.split()
						try:
								userid = re.sub("[^0-9]","",array[1])
						except:
								error = format_exc()
								if "IndexError" in error:
										await client.send_message(message.channel, usage)
										return #end command
								else:
										await client.send_message(message.channel, """Error while formatting mention into user id.
`"""+error+"`")
										consoleOutput(error)
										return

						if len(array) != 2:
								await client.send_message(message.channel, usage)
								return
						value = userData.get_user_data(userid,"criminality")
						await client.send_message(message.channel, "Criminality value for <@"+userid+"> is "+str(value)+".")
						consoleOutput("Criminality value is now "+str(value)+".")
		elif command.startswith(commandprefix+"set_crime"):
						usage = "Usage: "+commandprefix+"set_crime <mention> <value>"
						array = message_content.split()
						try:
								userid = re.sub("[^0-9]","",array[1])
						except:
								error = format_exc()
								if "IndexError" in error:
										await client.send_message(message.channel, usage)
										return #end command
								else:
										await client.send_message(message.channel, """Error while formatting mention into user id.
`"""+error+"`")
										consoleOutput(error)
										return
						if len(array) != 3:
								await client.send_message(message.channel, usage)
								return
						value = array[2]
						userData.set_user_data(userid,"criminality",value)
						await client.send_message(message.channel, "Updated criminality value for <@"+userid+"> to "+str(value)+".")
						consoleOutput("Updated value to "+str(value)+".")
		elif command.startswith(commandprefix+"change_crime"):
						usage = "Usage: "+commandprefix+"change_crime <mention> <value>"
						array = message_content.split()
						try:
								userid = re.sub("[^0-9]","",array[1])
						except:
								error = format_exc()
								if "IndexError" in error:
										await client.send_message(message.channel, usage)
										return #end command
								else:
										await client.send_message(message.channel, """Error while formatting mention into user id.
`"""+error+"`")
										consoleOutput(error)
										return

						if len(array) != 3:
								await client.send_message(message.channel, usage)
								return

						prevvalue = userData.get_user_data(userid,"criminality")
						value = array[2]
						if (type(prevvalue)) == str:
								prevvalue = 0
						if (type(value)) == str:
								value = 0
						finalvalue = prevvalue+value
						userData.set_user_data(userid,"criminality",finalvalue)

						await client.send_message(message.channel, "Changed criminality value for <@"+userid+"> by "+str(value)+" to equal "+str(finalvalue)+".")
						consoleOutput("Changed criminality value by "+str(value)+" to equal "+str(finalvalue)+".")

		#exclusive management commands. foolproofing isnt required since only i can use them
		elif command == commandprefix+"shutdown":
						#id check
						if isAdmin(message.author.id):
								await client.send_message(message.channel, "Access granted. Shutting down bot.")
								consoleOutput("Access granted. Shutting down bot.")
								await client.change_presence(status=discord.Status.invisible)
								sleep(2)
								force_exit(0)
						else:
								await reportAccessDenied(message)
								consoleOutput("Access denied.")
		elif command.startswith(commandprefix+"getuserdata"):
						#id check
						if isAdmin(message.author.id):
								array = message_content.split()
								userid = re.sub("[^0-9]","",array[1])
								await client.send_message(message.channel, "Access granted.")
								consoleOutput("Access granted.")
								value = str(userData.get_user_data(userid,array[2]))
								await client.send_message(message.channel, "Value stored with name '"+array[2]+"' for <@"+userid+"> is "+value)
								consoleOutput("Value stored is "+value)
						else:
								await reportAccessDenied(message)
								consoleOutput("Access denied.")
		elif command.startswith(commandprefix+"setuserdata"):
						#id check
						if isAdmin(message.author.id):
								array = message_content.split()
								userid = re.sub("[^0-9]","",array[1])
								await client.send_message(message.channel, "Access granted. Setting user data for <@"+userid+">.")
								consoleOutput("Access granted. Setting user data.")
								userData.set_user_data(userid,array[2],array[3])
								await client.send_message(message.channel, "Updated value.")
								consoleOutput("Updated value.")
						else:
								await reportAccessDenied(message)
								consoleOutput("Access denied.")
		elif command.startswith(commandprefix+"exec"):
						#id check
						if isAdmin(message.author.id):
								await client.send_message(message.channel, "Access granted. Executing command...")
								consoleOutput("Access granted. Executing command...")
								cmd = message_content[len(commandprefix)+5:]
								output = str(bytes(str(shell_exec(cmd, shell=True, stdout=SUB_PIPE).stdout.read()), "utf-8").decode("unicode_escape"))
								#trim "b' " and "'" from start and end.
								output = output[3:]
								output = output[:-1]
								#send it :D
								await client.send_message(message.channel, """```
"""+output+"```")
						else:
								await reportAccessDenied(message)
								consoleOutput("Access denied.")

		#if none of the above worked, check if it actually had the command prefix. if not, ignore it. if it did, report unknown command.
		elif command.startswith(commandprefix):
						await client.send_message(message.channel, "Unknown command '"+command+"'.")

		#triggerwords
		if "meep" in message_content.lower() and "list_" not in message_content.lower(): #prevents >list_meeps from triggering.
				await client.send_message(message.channel, "Meep")
				userData.set_user_data(message.author.id,"meeps",int(userData.get_user_data(message.author.id,"meeps"))+1)
		if "wheatley"  in message_content.lower() and "moron" in message_content.lower(): #message must have the words "wheatley" and "moron" to trigger.
				await client.send_message(message.channel,"I AM NOT A MORON!")
		if "pineapple" in message_content.lower():
				await client.send_message(message.channel,"""```
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
		if "no u" in message_content.lower() or "no you" in message_content.lower():
				await client.send_file(message.channel, fp="images\\no_u.jpg")
		if "the more you know" in message_content.lower():
				await client.send_file(message.channel, fp="images\\moreyouknow.gif")

	except:
		error = format_exc()
		await client.send_message(message.channel, """Internal error while running command! Error traceback:
`"""+error+"`")
		consoleOutput(error)
			
#get the bot token from the external file
for line in open("api_secret.token").readlines():
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