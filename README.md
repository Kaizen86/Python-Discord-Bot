# Wheatley Discord Bot
This is a Discord bot I made in Python. It is based of the discord.py library and was created more or less for fun and to add moderation utilities that me or my friends find useful in our servers. It is named after and has the icon of the Wheatley Core from Portal 2. I did that because I thought it was funny, to be honest.


Please be aware that this is intended to be compiled with PyInstaller.


## History
Wheatley has existed for a long time, first popping into existence on the 11th of November, 2017. That was back when I first bought a software package on Steam called [Discord Bot Maker](https://store.steampowered.com/app/682130/Discord_Bot_Maker/), which is based on NodeJS. At first, it was actually called Bender, but at some point I got the idea to call it Wheatley instead.

Over time the number of commands grew and grew, and Wheatley was on several servers. It was going so well... until I decided to try to upload the source code to GitHub.

#### 12th June 2018, 15:27-15:41: 'The Hack'
Let me tell a story when I accidentally leaked the API token back in 2018.

You see, when I uploaded the source code, I forgot to remove the hard coded bot token. I also did not know that people make web crawlers specifically to find these tokens that unsuspecting developers leak. I was on Discord on my phone at the time and I was startled when the channel I was scrolling on just disappeared. On the left hand side the list of channels rapidly shrank. The server was being deleted. The first thing I thought was: `"That can't be good"`. The next few minutes were total chaos as every channel in every server Wheatley was in was being nuked. My phone rung as my friend had also realised what was happening. On the phone he was panicked and confused, as was I. I had to explain to him that Wheatley had indeed been hacked. I tried to revoke the token to stop the firehose of delete commands. I was too late.

I have since added several preventative measures to stop this from ever happening again:
* Using an external file to hold the token instead of a string in the main script.
* Because of this external file, I would need to run `git add api_secret.token` to add the file to a commit.
* Using a throwaway test bot account and dedicated server to make a leak of the token an insignificant event.

**If you find a security bugs anywhere please contact me about it directly.**

## Commands
Below is a copy of the bot help, containing a list of commands.

General Commands
```
These commands do not have a classification.
	Display this help.
	>help
	Tests if the bot is working.
	>test
	Rolls a dice with an optional minimum and maximum limits.
	>dice [minimum] [maximum]
	Gives advice on where to find oxygen. In other words, the perfect command.
	>oxygen
	Tosses a coin. That's it.
	>coin_toss
	Reverses the given text.
	>reverse <text>
	Gets information about a mentioned user.
	>info <mention>
	Gets the avatar of a mentioned user.
	>avatar <mention>
	Play a game of rock paper scissors with the bot. (I promise it doesn't cheat)
	>rps <rock/paper/scissors>
	Gets the bot to repeat the input text. The bot will then try and delete your message to make it look real.
	>say <text>
	Gets the number of times the mentioned user has "meeped".
	>list_meeps <mention>
	Generates a Minecraft achievement with a random icon, with text based on the input.
	>mca <text>
	This command allow translation to and from Basic Shadow, which is a language invented by <@284415695050244106>.
	>translate <to/from> <English>
	Generates an ASCII art of the input text.
	>figlet <text>
	Gets a Wikipedia page on a topic.
	>wikipedia <topic>
	Deletes a certain number of messages in the same channel that the command was sent.
	>purge <number of messages>
```

Image manipulation commands
```
	>beauty <mention>
	>protecc <mention>
```

Voice channel commands
```
Rickrolls the voice channel you are connected to.
	>rickroll
	Plays a youtube video either from a URL or from a search term. Please be aware THIS IS NOT STABLE!!
	>play <url/search term>
	Disconnects the bot from the connected voice channel.
	>disconnect
```

Criminality Commands
```
These commands control or list the criminality values of a user.
	>list_crime <mention>
	>set_crime <mention> <value>
	>change_crime <mention> <increment value by>
```

Trigger Words
```
These are words that have make the bot do something if you say them.
	"meep"
	"wheatley" AND "moron"
	"pineapple"
	"no u" OR "no you"
	"the more you know"
```

Bot Administration Commands
```
These commands are intended for the bot owners. Accessing them will send a warning to the owner.
	Shutdown the bot.
	>shutdown
	Retrieve stored value for user attribute in database.
	>getuserdata <mention> <attribute>
	Update stored value for user attribute in database.
	>setuserdata <mention> <attribute> <value>
	Execute a shell command on the host computer.
	>execute <shell command>
	Reloads the bot configuration files. Useful for applying changes.
	>reload
```

## Dependencies
Run 'pip install' on all of these packages to install them:
- discord (the rewrite branch)
- asyncio
- Pillow
- requests
- pyfiglet
- youtube-dl
- wikipedia

Compiling using the batch file will require PyInstaller.
