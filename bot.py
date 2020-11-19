#!/usr/bin/python3
print("Program is now executing.")

import discord
from discord.ext import commands
import asyncio
from traceback import format_exc

command_prefix = "."

#Array of cogs to load
extensions = [
	'cogs.voice',
	'cogs.admin'
]

#Open token file and extract the token
token_filename = "api_secret.token"
try:
	token_lines = open(token_filename,"r").readlines()
except:
	#Readlines failed, probably missing file.
	exit("""
Token file missing, aborting.
Create the '{0}' file containing the bot token and retry.""".format(token_filename))
else:
	#We loaded something, find the token in the file.
	token = None
	for line in token_lines:
		#Ignore commented lines or empty lines
		if not (line.startswith("#") or line.isspace() or len(line) == 0):
			token = line
if token is None: exit(token_filename+" does not contain a token.")
else: print("Loaded token.")

#Initialise bot client
bot = commands.Bot(
	command_prefix=commands.when_mentioned_or(command_prefix),
	description="Wheatley Discord Bot, now with extra cogs!"
)

#Load cogs
for extension in extensions:
	print("Loading:\t"+extension,end=" ")
	try: bot.load_extension(extension)
	except:
		print("[ERROR]")
		print(format_exc())
	else: print("[OK]")
print("All extensions loaded.\nRunning bot.")

#Set the custom status to say how to get help when the bot loads
@bot.event
async def on_ready():
	print("Bot ready.")
	await bot.change_presence(
		status=discord.Status.online,
		activity=discord.Game(name=command_prefix+"help")
	)
#Start bot using the token
bot.run(token)
