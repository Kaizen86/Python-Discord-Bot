#!/usr/bin/python3
print("Program is now executing.")

import discord
from discord.ext import commands
import asyncio

#Array of cogs to load
extensions = [
    'cogs.test'
]

#Open token file and extract the token
token_filename = "api_secret.token"
try:
    token_lines = open(token_filename,"r").readlines()
except:
    exit("""
Token file missing, aborting.
Create the '{0}' file containing the bot token and retry.""".format(token_filename))
else:
    token = None
    for line in token_lines:
        #ignore commented lines or empty lines
        if not (line.startswith("#") or line.isspace() or len(line) == 0):
            token = line
if token is None: exit(token_filename+" does not contain a token.")
else: print("Loaded token.")

#Initialise bot client
bot = commands.Bot(
	command_prefix=commands.when_mentioned_or("."),
	description="Simple test bot for Cogs"
)

#Load cogs
for extension in extensions:
    print("Loading extension: "+extension)
    bot.load_extension(extension)

#Start bot using the token
bot.run(token)
