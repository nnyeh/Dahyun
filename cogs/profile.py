import discord
from discord.ext import commands
from data import database as db

class profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["pf"])
    async def profile(self, ctx, arg=None):

        if arg is None:
            username = db.get_user(ctx.author.id)
        else:
            username = db.get_user(ctx.message.mentions[0].id)

        if username is None:
            embed = discord.Embed(description = f"You need to first set your Last.fm username with the command\n`>set [your username]`", colour = 0x4a5fc3)
            return await ctx.send(embed=embed)

        lastfm_username = username [0][1];

        await ctx.send(f"https://www.last.fm/user/{lastfm_username}")

async def setup(bot):
    await bot.add_cog(profile(bot))