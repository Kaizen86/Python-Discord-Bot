from datetime import datetime
from traceback import format_exc
from discord.ext import commands
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

		if user_request.startswith("#"):
			await ctx.send("lmao coming soon")
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

			# Parse the request
			list = json.loads(response.read())
			colours = list["colors"]
			if len(colours) > 0:  # Was anything sent back?
				for colour in colours:  # What about if there's an exact match?
					if colour["name"] == user_request.title():
						hex_code = colour["hex"]
						break
				else:  # Pick the first one I guess
					await ctx.send(str(colours[0]))
			else:  # Inform the user we couldn't find anything
				await ctx.send("Sorry, couldn't find a match.")

			""" At this point, hex_code contains the colour to apply to the user.
			TODO: Implement this:
				Check if this user has a colour role already
					If they do, simple update it.
					Otherwise make a new role with the colour, assign them to it, and record that in a database
				"""
def setup(bot):
	bot.add_cog(RoleManagerCog(bot))
