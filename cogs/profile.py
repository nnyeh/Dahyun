import os
import requests
from discord.ext import commands
from data import database as db

class profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def profile(self, ctx, arg=None):

        if arg is None:
            username = db.get_user(ctx.author.id)
        else:
            username = db.get_user(ctx.message.mentions[0].id)

        if username is None:
            return await ctx.send(f"`You need to first set your Last.fm username with the command`\n```>set [your username]```")

        lastfm_username = username [0][1];
        params = {
            "user": lastfm_username,
            "api_key": os.getenv("LASTFM_API_KEY"),
            "format": "json",
            "method": "user.getInfo"
        }

        r = requests.get("http://ws.audioscrobbler.com/2.0/", params=params)
        data = r.json()
        link = data["user"]["url"]

        await ctx.send(link)

def setup(bot):
    bot.add_cog(profile(bot))