from datetime import datetime
from traceback import format_exc
from discord import Colour
from discord.ext import commands
from discord.utils import get
import database.Database as db
import re
import urllib.request
import urllib.parse
import json

def time():
	"""Returns a formatted timestamp suitable for use in log functions"""
	return datetime.now().strftime("%m/%d %H:%M:%S ")

class RoleManagerCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(
		usage="[name or hex code]"
	)
	async def colour(self, ctx, *, user_request: str = None):
		"""Changes your name to have a custom colour.

You can either provide the name of a colour, in which case we will attempt to find it,
or you can specify the precise hex code starting with a #"""
		def log(string):
			print(time() + "[RoleManage.colour] " + str(string))

		if user_request[0] == "#":
			if not re.search('[0-9a-zA-Z]{6}', user_request[1:]):
				await ctx.send("Sorry, but that does not seem to be a valid hex code")
				return
			hex_code = user_request  # Directly set it, we're about to format hex_code anyway.
		else:
			# Convert spaces and maybe other characters to % codes
			quoted = urllib.parse.quote(user_request)

			# Construct a request to be sent
			url = "https://api.color.pizza/v1/names/{}?goodnamesonly=true".format(quoted)
			req = urllib.request.Request(
				url,
				data=None,
				headers={
					# In the face of error 403, we lie. This is the user agent from my browser.
					'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0'
				}
			)
			# Send API request
			try:
				response = urllib.request.urlopen(req, timeout=2)
			except urllib.error.URLError:
				log("Error, cannot contact api.color.pizza. traceback is:\n" + format_exc())
				await ctx.send("Failure to send colour name resolution request ( o_O)")
				return

			# Parse the request
			list = json.loads(response.read())
			colours = list["colors"]
			if len(colours) > 0:  # Was anything sent back?
				for colour in colours:  # What about if there's an exact match?
					if colour["name"] == user_request.title():
						hex_code = colour["hex"]
						break
				else:  # Pick the first one I guess
					hex_code = str(colours[0]["hex"])
			else:  # Inform the user we couldn't find anything
				await ctx.send("Sorry, couldn't find a match")
				return

		# Convert the hex code into an integer, suitable to be passed to discord.py
		colour = int("0x" + hex_code[1:], base=16)  # [1:] strips the #
		if colour == 0:  # There's an edge case where 0 will clear the colour instead of making it black...
			colour = 1  # So we give a tiny amount of blue instead.

		# Check if the user has a colour role already
		guild_db = db.guilds[ctx.guild.id]
		role_id = guild_db.read(ctx.author.id)
		if role_id:
			msg = await ctx.send("Yep sure thing!")
			# Try to use the role associated with the user
			role = get(ctx.guild.roles, id=role_id)
			if role:
				# Update the role's colour
				await role.edit(
					reason="Updating colour role - " + user_request,
					colour=Colour(colour))

				# Make sure the user has the role assigned to them
				for user_role in ctx.author.roles:
					if user_role.id == role.id:
						break  # Found a match, stop searching
				else:
					# If the search concluded with no break, they don't have the role.
					await ctx.author.add_roles(role, reason="Correcting absence of colour role from user")
			else:
				# Invalidate the role id so a new one is made
				role_id = None
				await msg.edit(content=msg.content + "\nlmao an Admin deleted it")

		if not role_id:
			# Make a new role with the colour and assign it to the user
			msg = await ctx.send("Alrighty, I'll go ahead and make a new role just for you :)")
			role = await ctx.guild.create_role(
				name=ctx.author.name,  # Call it whatever their username is
				reason="Generating new colour role - " + user_request,
				colour=Colour(colour),
				hoist=True)  # Try to make it visible

			# Record the role id in the database alongside the user's id.
			guild_db.write(ctx.author.id, role.id)
			guild_db.save()

			# Assign it to a user
			await ctx.author.add_roles(
				role,
				reason="Assigning new colour role to user")

			# Determine where the new role should go; right under ours.
			def FindHighestRolePosition(roles):
				pos = 0
				for role in roles:
					if role.position > pos:
						pos = role.position
				return max(0, pos - 1)
			position = FindHighestRolePosition(ctx.me.roles)

			# Elevate role to highest permittable to ensure it takes precedence
			if position != 0:  # Only if its possible to change anything
				await ctx.guild.edit_role_positions(positions={role: position})
			await msg.edit(content=msg.content + "\nAll done!")

def setup(bot):
	bot.add_cog(RoleManagerCog(bot))
