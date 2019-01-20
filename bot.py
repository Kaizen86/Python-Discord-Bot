print("Program is now executing.")
lengthofthisfile = 207

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

print("Loading vital...")
import discord #This uses the rewrite of the discord module that supports 3.7
import asyncio

print("Loading sub-vital...")
#sub-vital
from traceback import format_exc #for error handling
from modules import database #for all database controls

consoleOutput("Loading commands and their libraries...")
import commands #Load all the commands and their code from the commands.py file
from time import sleep #bot loop
from modules import shadow_translator #translate (i made this one :D)

consoleOutput("Modules loaded. Loading configs...")
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
verifyFolderExistence("databases")
userData = database.Database("databases\\users.json")
shadowtranslator = shadow_translator.ShadowTranslator()

#custom error class for comedic purposes in hilariously catastrophic scenarios
class ExcuseMeWhatTheFuckError(Exception):
    pass
	
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

		#convert any unicode to ascii. quick and dirty way to prevent codec errors
		author_name = message.author.name.encode('ascii','ignore').decode('ascii','ignore')
		message_content = message.content.encode('ascii','ignore').decode('ascii','ignore')

		try:
			command = message_content.lower().split()[0][len(commandprefix):]
		except:
			#bot joins / emoji throws an exception, so this ignores that.
			return

		#log command usage
		if message_content.startswith(commandprefix):
			consoleOutput(author_name + " executed command  " + message_content)
			#start the bot 'typing'. this gives feedback that the bot is calculating the command output.
			await message.channel.trigger_typing() #typing stops either after 10 seconds or when a message is sent.

			#https://stackoverflow.com/questions/35484190/python-if-elif-else-chain-alternitive
			mydict = {'help':commands.help, 'test':commands.test, "shutdown":commands.shutdown}
			if command in mydict:
				action = mydict[command]
				# set up args from the dictionary .
				await action(message,commandprefix)
			else:
				#if none of the above worked, report unknown command.
				await message.channel.send("Unknown command '"+command+"'.")

		#triggerwords
		if "meep" in message_content.lower() and "list_" not in message_content.lower(): #prevents >list_meeps from triggering.
				await message.channel.send("Meep")
				userData.set_user_data(message.author.id,"meeps",int(userData.get_user_data(message.author.id,"meeps"))+1)
		if "wheatley"  in message_content.lower() and "moron" in message_content.lower(): #message must have the words "wheatley" and "moron" to trigger.
				await message.channel.send("I AM NOT A MORON!")
		if "pineapple" in message_content.lower():
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
		if "no u" in message_content.lower() or "no you" in message_content.lower():
				await message.channel.send_file(message.channel, fp="images\\no_u.jpg")
		if "the more you know" in message_content.lower():
				await message.channel.send_file(message.channel, fp="images\\moreyouknow.gif")

	except:
		error = format_exc()
		await message.channel.send("""Internal error while running command! Error traceback:
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