#!/usr/bin/python3
print("Program is now executing.")

import discord
from discord.ext import commands
import asyncio

#Array of cogs to load
extensions = [
    'cogs.voice'
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
	command_prefix=commands.when_mentioned_or("."),
	description="Simple test bot for Cogs"
)

#Load cogs
print("Loading extensions...")
for extension in extensions:
    print("\t"+extension)
    bot.load_extension(extension)
print("All extensions loaded.\nRunning bot.")

#Start bot using the token
bot.run(token)
