from discord.ext import commands
from data import database as db

class unsetusername(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def unset(self, ctx):
        
        db.update_user(ctx.author.id, "lastfm_username", None)

        await ctx.send(f"{ctx.author.mention}`, your Last.fm username has been unset` <a:DubuRito:773333382918569984>")

def setup(bot):
    bot.add_cog(unsetusername(bot))