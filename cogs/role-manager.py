from datetime import datetime
from traceback import format_exc
from discord import Colour
from discord.ext import commands
from discord.utils import get
import database.Database as db
import re
import urllib
import json

def time():
    """Returns a formatted timestamp suitable for use in log functions"""
    return datetime.now().strftime("%m/%d %H:%M:%S ")

class RoleManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def FindHighestRolePosition(self, roles):
        pos = 0
        for role in roles:
            if role.position > pos:
                pos = role.position
        return max(0, pos - 1)

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
        def log(string):
            print(time() + "[RoleManage.colour] " + str(string))

        # Find the user's colour role, if it exists.
        guild_db = db.guilds[ctx.guild.id]
        role_id = guild_db.read(ctx.author.id)
        role = get(ctx.guild.roles, id=role_id)

        if user_request == "remove":
            # User wants to delete their colour role entirely
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

        elif user_request[0] == "#":
            if not re.search('[0-9a-zA-Z]{6}', user_request[1:]):
                await ctx.send("Sorry, but that does not seem to be a valid hex code")
                return
            hex_code = user_request  # Directly set it, we're about to format hex_code anyway.

        else:
            try:
                hex_code = self.LookupColourName(user_request)
            except urllib.error.URLError:
                log("Error, cannot contact api.color.pizza. traceback is:\n" + format_exc())
                await ctx.send("Failure to send colour name resolution request ( o_O)")
                return

            if not hex_code:
                await ctx.send("Sorry, couldn't find a match")
                return

        # Convert the hex code into an integer, suitable to be passed to discord.py
        colour = int("0x" + hex_code[1:], base=16)  # [1:] strips the #
        if colour == 0:  # There's an edge case where 0 will clear the colour instead of making it black...
            colour = 1  # So we give a tiny amount of blue instead.

        # Check if the user has a colour role already
        if role:
            msg = await ctx.send("Yep sure thing!")
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
                return

        else:
            # Make a new role with the colour and assign it to the user
            msg = await ctx.send("Alrighty, I'll go ahead and make a new role just for you :)")
            role = await ctx.guild.create_role(
                name=ctx.author.name,  # Call it whatever their username is
                reason="Generating new colour role - " + user_request,
                colour=Colour(colour))  # Of course, give it the custom colour

            # Record the role id in the database alongside the user's id.
            guild_db.write(ctx.author.id, role.id)
            guild_db.save()

            # Assign it to a user
            await ctx.author.add_roles(
                role,
                reason="Assigning new colour role to user")

            # Determine where the new role should go; right under ours.
            position = self.FindHighestRolePosition(ctx.me.roles)

            # Elevate role to highest permittable to ensure it takes precedence
            if position != 0:  # Only if its possible to change anything
                await ctx.guild.edit_role_positions(positions={role: position})

        await msg.edit(content=msg.content + "\nAll done!")

    @commands.command(
        usage="[role ids to disentangle]"
    )
    @commands.has_permissions(manage_roles=True)
    async def extricate(self, ctx, *, user_request: str = ""):
        msg = await ctx.send("Initialising.")

        guild_db = db.guilds[ctx.guild.id]  # Get this server's role database

        roles = dict()
        for word in user_request.split(" "):
            if word.isdigit():
                id = int(word)
                roles[id] = ctx.guild.get_role(id)
            else:
                await msg.edit(content=msg.content + "\n  Ignoring non-ID '{}'".format(word))
        if len(roles) == 0:
            await msg.edit(content=msg.content + "\nNo IDs present, aborting.")
            return

        msg = await ctx.send("Role disentanglement in progress!")
        for id in roles:
            role = roles[id]
            await msg.edit(content=msg.content + "\n  {}: {} members".format(
                role.name, len(role.members)))
            for member in role.members:
                await msg.edit(content=msg.content + "\n    {}".format(
                    member.name))
                # Make a new role with the colour and assign it to the user
                new_role = await ctx.guild.create_role(
                    name=member.name,  # Call it whatever their username is
                    reason="Generating new colour role - extrication process",
                    colour=role.colour)  # Give it the colour of the old role
                # Record the role id in the database alongside the user's id.
                guild_db.write(member.id, new_role.id)
                # Assign it to a user
                await member.add_roles(
                    new_role,
                    reason="Assigning new colour role to user")

                # Determine where the new role should go; right under ours.
                position = self.FindHighestRolePosition(ctx.me.roles)

                # Elevate role to highest permittable to ensure it takes precedence
                if position != 0:  # Only if its possible to change anything
                    await ctx.guild.edit_role_positions(positions={new_role: position})
            await role.delete()  # Remove the old role after processing all members

        guild_db.save()  # Save the database to disk
        await ctx.send("Finished. All old colour roles have been migrated successfully!")

def setup(bot):
    bot.add_cog(RoleManagement(bot))
