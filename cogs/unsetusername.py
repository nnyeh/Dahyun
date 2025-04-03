import discord
from discord.ext import commands
from data import database as db

class unsetusername(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def unset(self, ctx):
        
        db.update_user(ctx.author.id, "lastfm_username", None)

        embed = discord.Embed(description = f"Your Last.fm username has been unset <a:DubuRito:773333382918569984>", colour = 0x4a5fc3)
        await ctx.send(f"{ctx.author.mention}", embed=embed)

async def setup(bot):
    await bot.add_cog(unsetusername(bot))