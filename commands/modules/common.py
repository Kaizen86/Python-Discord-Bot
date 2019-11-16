from time import localtime #file logs
from os import listdir #folder existence checks
from os import mkdir #make new folder if needed
from os import remove as delete_file #uploadImageFromObject()
import re #used to remove non-numbers from mentions to extract the user id
from traceback import format_exc #for error handling

def verifyFolderExistence(foldername):
	if foldername not in listdir():
		print("Making '"+foldername+"' folder.")
		mkdir(foldername)

#generate the filepath of the current log file
def generateLogfileName(): 
	time = localtime()
	return F"logs/log_{time[0]}-{time[1]}-{time[2]}.txt" #determine which log file we should write to based on the date
	
def consoleOutput(text, *args, **kwargs): #consoleOutput is encouraged as a replacement of print as it writes everything to a log file.
	#following "The Great Disconnect" (the Pi disconnected from WiFi and 
	#filled the disk with 18GB of errors), it now store logs in separate files.
	time = localtime()
	logfilename = F"logs/log_{time[0]}-{time[1]}-{time[2]}.txt" #determine which log file we should write to based on the date
	#format text to have timestamp
	text = F"{time[0]}/{time[1]}/{time[2]} {time[3]}:{time[4]}:{time[5]}: {text}"
	#prints to the console
	print(text)
	#write to log
	logfile = open(logfilename,"a")
	logfile.write(text+"\n")
	logfile.close()
	
#custom error class for comedic purposes in hilariously catastrophic scenarios
class ExcuseMeWhatTheFuckError(Exception): pass

#extract a user id from a string using regex
def getUserId(string): return re.sub("[^0-9]","",string)

async def uploadImageFromObject(image,message):
	#unfortunately you cannot send a pillow object using discord.py directly. it must be loaded from a file.
	imageid = str(randint(1,99999999))+".png"  #just to make sure nothing is overwritten in heavy loads.
	try:
		image.save(imageid) #save it...
		await message.channel.send(file=discord.File(imageid, filename="img.png")) #then send the image.
	except:
		await message.channel.send("Error while trying to send image.")
		consoleOutput(format_exc())
	finally:
		delete_file(imageid) #delete the file afterwards.