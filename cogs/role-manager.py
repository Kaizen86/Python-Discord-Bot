import logging
from traceback import format_exc
import discord
from discord.ext import commands
from discord.utils import get
from PIL import Image
import database.Database as db
import io
import json
import re
import urllib

class RoleManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def PillowImageToBytesIO(self, image):
        """Converts a Pillow Image object into a ByteIO object in PNG format.
    This operation is required for sending images to Discord's API"""
        image_binary = io.BytesIO()
        image.save(image_binary, "PNG")
        image_binary.seek(0)
        return image_binary

    def FindHighestRolePosition(self, roles):
        pos = 0
        for role in roles:
            if role.position > pos:
                pos = role.position
        return pos

    def LookupColourName(self, colour_name: str):
        # Convert spaces and maybe other characters to % codes
        quoted = urllib.parse.quote(colour_name)

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
        response = urllib.request.urlopen(req, timeout=2)

        # Parse the request
        list = json.loads(response.read())
        colours = list["colors"]
        if len(colours) > 0:  # Was anything sent back?
            for colour in colours:  # What about if there's an exact match?
                if colour["name"] == colour_name.title():
                    return colour["hex"]
            else:  # Pick the first one I guess
                return str(colours[0]["hex"])
        else:  # Return None, we couldn't find anything.
            return None

    @commands.command(
        usage="[colour name or hex code]"
    )
    async def colour(self, ctx, *, user_request: str = None):
        """Changes your name to have a custom colour.

You can either provide the name of a colour, in which case we will attempt to find it,
or you can specify the precise hex code starting with a #

Should you want to remove your colour role, you can do that by saying "remove" instead of a colour."""
        # Find the user's colour role, if it exists.
        guild_db = db.guilds[ctx.guild.id]
        role_id = guild_db.read(ctx.author.id)
        role = get(ctx.guild.roles, id=role_id)

        if user_request is None:
            # No parameters were supplied, show an embed with their colour
            embed = discord.Embed()
            if role:
                embed.title = "Your colour:"
                embed.colour = role.colour
                # Create a small image with the colour and attach it to the embed
                colour_thumbnail = Image.new(
                    "RGB",
                    size=(128, 128),
                    color=(role.colour.r, role.colour.g, role.colour.b))
                file = discord.File(self.PillowImageToBytesIO(colour_thumbnail), filename="image.png")
                embed.set_image(url="attachment://image.png")  # Turns out the URL can reference attachments, what fun!
                # Send the embed and the colour colour_thumbnail
                await ctx.send(file=file, embed=embed)
            else:
                await ctx.send("""At the moment, you do not have a colour role.
Instructions for using this command can be found using the 'help' command.""")
            return  # Stop here

        # Check if they want to delete their colour role entirely
        elif user_request == "remove":
            # Check if the user has a colour role
            if role:
                # Delete the role
                await role.delete(
                    reason="Deleted at request of user")
                await ctx.send("Role has been removed")
                return
            else:
                await ctx.send("As far as I know, you don't have a colour role.")
                return

        # Check if they are trying to specify a own colour code
        elif user_request[0] == "#":
            if not re.search('[0-9a-zA-Z]{6}', user_request[1:]):
                await ctx.send("Sorry, but that does not seem to be a valid hex code")
                return
            hex_code = user_request  # Directly set it, we're about to format hex_code anyway.

        # In all other circumstances, they have given the name of the colour for us to lookup.
        else:
            try:
                hex_code = self.LookupColourName(user_request)
            except urllib.error.URLError:
                logging.error("Cannot contact api.color.pizza. traceback is:\n" + format_exc())
                await ctx.send("Failure to send colour name resolution request ( o_O)")
                return

            if not hex_code:
                await ctx.send("Sorry, couldn't find a match")
                return

        # Convert the hex code into an integer, suitable to be passed to discord.py
        colour = int("0x" + hex_code[1:], base=16)  # [1:] strips the #
        if colour == 0:  # There's an edge case where 0 will clear the colour instead of making it black...
            colour = 1  # So we give a tiny amount of blue instead. Nobody will notice that, right?

        # Check if the user has a colour role already
        if role:
            msg = await ctx.send("Yep sure thing!")
            # Update the role's colour
            await role.edit(
                reason="Updating colour role - " + user_request,
                colour=discord.Colour(colour))

            # Make sure the user has the role assigned to them
            for user_role in ctx.author.roles:
                if user_role.id == role.id:
                    break  # Found a match, stop searching
            else:
                # If the search concluded with no break, they don't have the role.
                await ctx.author.add_roles(role, reason="Correcting absence of colour role from user")
                return

        else:
            # Make a new role with the colour and assign it to the user
            msg = await ctx.send("Alrighty, I'll go ahead and make a new role just for you :)")
            role = await ctx.guild.create_role(
                name=ctx.author.name,  # Call it whatever their username is
                reason="Generating new colour role - " + user_request,
                colour=discord.Colour(colour))  # Of course, give it the custom colour

            # Record the role id in the database alongside the user's id.
            guild_db.write(ctx.author.id, role.id)
            guild_db.save()

            # Assign it to a user
            await ctx.author.add_roles(
                role,
                reason="Assigning new colour role to user")

            # Determine where the new role should go; right under our topmost role.
            position = self.FindHighestRolePosition(ctx.me.roles)

            # If the role position is 2 or lower then we can't move it anywhere
            # (Role indexes count upwards from 1, and since we just made a role it can only be as low as 2)
            if position > 2:
                try:
                    # Attempt to move
                    await ctx.guild.edit_role_positions(positions={role: position - 1})
                except:
                    await ctx.send(":thinking: I can't move your role around which is a bit odd, but I'll ignore that.")

            await msg.edit(content=msg.content + "\nAll done!")

def setup(bot):
    bot.add_cog(RoleManagement(bot))
