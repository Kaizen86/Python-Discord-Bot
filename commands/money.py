from commands.modules.common import *
from traceback import format_exc #for error handling

async def balance(globaldata):
	message = globaldata["message"]
	commandprefix = globaldata["commandprefix"]
	userData = globaldata["userData"]

	usage = "Usage: {0}balance [mention]".format(commandprefix)
	array = message.content.split()
	#use either the message author id or the user they specified if any.
	if len(array) > 1:
		userid = getUserId(array[1])
	else:
		userid = message.author.id
	value = userData.get_user_data(userid,"money")
	await message.channel.send("Balance for <@{0}> is {1} credits.".format(userid,value))

#admin only commands
async def add_money(globaldata):
	message = globaldata["message"]
	commandprefix = globaldata["commandprefix"]
	userData = globaldata["userData"]

	usage = "Usage: {0}add_money <value> [mention]".format(commandprefix)
	array = message.content.split()

	#Check for insufficient argument count
	if len(array) < 2:
		await message.channel.send(usage)
		return

	#attempt to convert value argument to an integer.
	try: value = int(array[1])
	except:
		await message.channel.send("Credit value must be a number.\n"+usage)
		return

	#use either the message author id or the user they specified if any.
	if len(array) > 2: userid = getUserId(array[2])
	else: userid = message.author.id

	prev_money = userData.get_user_data(userid,"money")
	new_money = prev_money + value
	userData.set_user_data(userid,"money",new_money) #write change to database
	await message.channel.send(
		"Balance for <@{0}> was {1}, is now {2}.".format(
		userid, prev_money, new_money))

async def set_money(globaldata):
	message = globaldata["message"]
	commandprefix = globaldata["commandprefix"]
	userData = globaldata["userData"]

	usage = "Usage: {0}set_money <value> [mention]".format(commandprefix)
	array = message.content.split()

	#Check for insufficient argument count
	if len(array) < 2:
		await message.channel.send(usage)
		return

	#attempt to convert value argument to an integer.
	try: value = int(array[1])
	except:
		await message.channel.send("Credit value must be a number.\n"+usage)
		return

	#use either the message author id or the user they specified if any.
	if len(array) > 2: userid = getUserId(array[2])
	else: userid = message.author.id

	prev_money = userData.get_user_data(userid,"money")
	userData.set_user_data(userid,"money",value) #write change to database
	await message.channel.send(
		"Balance for <@{0}> was {1}, is now {2}.".format(
		userid, prev_money, value))

async def globalset_money(globaldata):
	message = globaldata["message"]
	commandprefix = globaldata["commandprefix"]
	userData = globaldata["userData"]

	usage = "Usage: {0}globalset_money <value>".format(commandprefix)
	array = message.content.split()

	#Check for insufficient argument count
	if len(array) < 2:
		await message.channel.send(usage)
		return

	#attempt to convert value argument to an integer.
	try: value = int(array[1])
	except:
		await message.channel.send("Credit value must be a number.\n"+usage)
		return

	await message.channel.send("Please wait, this may take a moment.")

	#apply value to all users
	for member in message.guild.members:
		userData.set_user_data(member.id,"money",value)
	await message.channel.send("Balance for all users is now {0}.".format(value))
