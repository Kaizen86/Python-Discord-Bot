#!/usr/bin/python3
print("Program is now executing.")

import discord
from discord.ext import commands
import asyncio


cog_list = [
    'cogs.test'
]

bot = commands.Bot(
	command_prefix=commands.when_mentioned_or("."),
	description="Simple test bot for Cogs"
)

for extension in cog_list:
    bot.load_extension(extension)

bot.run("NTM2NTMxOTAxMjc2NDg3Njkw.XERyRQ.pgNxeicn-JXfvqGyCmq6TNSizT8")
