import discord
from discord.ext import commands

class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        usage="[ping]"
    )
    async def avatar(self, ctx, *, user: discord.Member = None):
        """Get somebody's avatar.

Specify a user by pinging them, or leave it blank to use your own profile."""
        if not user:
            user = ctx.message.author

        # Construct and send embed
        embed = discord.Embed(title="Avatar for " + user.name + "#" + user.discriminator)
        embed.set_image(url=user.avatar_url)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Utilities(bot))
