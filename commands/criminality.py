from commands.modules.common import *
from traceback import format_exc #for error handling

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

