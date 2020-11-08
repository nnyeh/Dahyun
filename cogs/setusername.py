import os
import requests
from discord.ext import commands
from data import database as db

class setusername(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def set(self, ctx, username):
        params = {
            "user": username,
            "api_key": os.getenv("API_KEY"),
            "format": "json",
            "method": "user.getInfo"
        }

        r = requests.get("http://ws.audioscrobbler.com/2.0/", params=params)
        data = r.json()
        try:
            username = data["user"]["name"]
        except KeyError:
            return await ctx.send(f"`Invalid Last.fm username` <a:DubuAngry:773329674679746610>")

        db.update_user(ctx.author.id, "lastfm_username", username)
        await ctx.send(f"{ctx.author.mention}`, your Last.fm username has been set as {username}` <a:DubuFlirt:773331886461157427>")

def setup(bot):
    bot.add_cog(setusername(bot))