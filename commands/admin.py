from commands.modules.common import *
from traceback import format_exc #for error handling

from discord import Status #shutdown
from time import sleep #shutdown
from os import _exit as force_exit #shutdown
from subprocess import PIPE as SUB_PIPE #execute
from subprocess import Popen as shell_exec #execute
import shlex #execute

#exclusive management commands.
async def shutdown(passedvariables):
	#include all the required variables
	message = passedvariables["message"]
	client = passedvariables["client"]
	voiceclients = passedvariables["connectedvoicechannels"]

	await message.channel.send("Shutting down bot...")
	consoleOutput("Closing all voice clients...")
	i=1
	for id in voiceclients: #try to disconnect all the voice channels
		try:
			await voiceclients[id].disconnect()
			consoleOutput(F"Closed {i}/{len(voiceclients)} voice clients.")
			i+=1
		except Exception as err: consoleOutput("Error: "+str(err))
	consoleOutput("Shutting down.")
	await client.change_presence(status=Status.invisible)
	sleep(2)
	force_exit(0)

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
	#remove any characters past 1990 limit
	output = output[:1990]
	#send it
	await message.channel.send("""```
"""+output+"```")
