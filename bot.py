#!/usr/bin/python3
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%Y/%m/%d %I:%M:%S")

from traceback import format_exc, format_exception  # First one contextually processes excs., second one formats exc. objects
import asyncio
import discord
from discord.ext import commands
import database.Database as db

# Make sure we are running in the same directory as the script
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))

command_prefix = "-"  # If this is found at the start of the message, its a command for us
# List of cogs to load
extensions = [
    "cogs.role-manager",
    "cogs.utilities"
]

# Open token file and extract the token
token_filename = "api_secret.token"
try:
    token_lines = open(token_filename, "r").readlines()
except:
    # Readlines failed, probably missing file.
    exit("""
Token file missing, aborting.
Create the '{0}' file containing the bot token and retry.""".format(token_filename))
else:
    # We loaded something, find the token in the file.
    token = None
    for line in token_lines:
        # Ignore commented lines or empty lines
        if not (line.startswith("#") or line.isspace() or len(line) == 0):
            token = line
if token is None:
    exit(token_filename + " does not contain a token.")
else:
    logging.info("Loaded token.")

# Define our desired intents
intents = discord.Intents.default()
intents.members = True

# Initialise bot client
bot = commands.Bot(
    command_prefix=commands.when_mentioned_or(command_prefix),
    description="Felt cute, might flex on you <3",
    intents=intents
)

# Load cogs
for extension in extensions:
    output = "Loading:\t" + extension
    try:
        bot.load_extension(extension)
    except:
        logging.error(output + " [ERROR]\n" + format_exc())
    else:
        logging.info(output + " [OK]")
logging.info("All extensions loaded. Running bot.")

# Set the custom status to say how to get help when the bot loads
@bot.event
async def on_ready():
    logging.info("Bot ready.")
    # Load database files
    db.LoadAllFiles(bot)
    # Update presence
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game(name="Local flexpert, " + command_prefix + "help")
    )

# Send instructions when we join a new server
@bot.event
async def on_guild_join(guild):
    logging.info("Joined a new guild called {}!".format(guild.name))
    # Create brand new database object
    db.guilds[guild.id] = db.Database("{}.json".format(guild.id))

# Report when a command was run
@bot.event
async def on_command(ctx):
    logging.info("[bot] '{0}' executed command '{1}'".format(ctx.message.author.name, ctx.message.content))

# Ping me in the server when a command error occurs
@bot.event
async def on_command_error(ctx, exception):
    logging.error(exception)
    if type(exception) == commands.errors.CommandNotFound:
        await ctx.send("Sorry, I don't know what that is.\nRun the help command to see what I can do.")
        return
    # It's an unknown error, ping me.
    try:
        me = await ctx.guild.fetch_member(285465719292821506)
    except:
        # If I am not in the server then an exception will be thrown.
        logging.warn("Could not find Blattoid in the server")
        await ctx.send("Whoops, something broke. Please send Blattoid this message for me:\n" + str(exception))
    else:
        # If the try succeeded then I am present in the server and the 'me' variable will contain a valid member object.
        await ctx.send("Hey {0}, something went wrong in the code.\nHere is the error message: {1}".format(me.mention, exception))
    # Print the traceback to make debugging easier.
    logging.error(''.join(format_exception(
        type(exception),
        value=exception,
        tb=exception.__traceback__)))

# Start bot using the token
loop = asyncio.new_event_loop()
try:
    loop.run_until_complete(bot.run(token))
except:
    logging.info("[bot] Fatal exception caused bot crash.\n" + format_exc())
