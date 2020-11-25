import os
import discord
import requests
from discord.ext import commands
from data import database as db
from datetime import datetime

class genregetinfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["gi"])
    async def genreinfo(self, ctx, *, arg):

        username = db.get_user(ctx.author.id)

        if username is None:
            return await ctx.send(f"`You need to first set your Last.fm username with the command`\n```>set [your username]```")

        lastfm_username = username [0][1];
        if not lastfm_username:
            return await ctx.send(f"`You need to first set your Last.fm username with the command`\n```>set [your username]```")

        genre_info_params = {
            "tag": arg,
            "api_key": os.getenv("LASTFM_API_KEY"),
            "format": "json",
            "method": "tag.getInfo"
        }

        r = requests.get("http://ws.audioscrobbler.com/2.0/", params=genre_info_params)
        gidata = r.json()
        try:
            arg = gidata["tag"]["name"]
        except KeyError:
            return await ctx.send(embed = discord.Embed(
                description = f"This genre doesn't exist.",
                colour = 0x4a5fc3
                ))
        genre_name = arg.lower()
        genre_info = gidata["tag"]["wiki"]["content"]

        genre_info = genre_info.strip()
        sep = "<a"
        genre_info = genre_info.split(sep, 1)[0]
        if len(genre_info)>800:
            genre_info = genre_info[:800] + "..."

        now = datetime.now()
        timestamp = now.strftime("%#H:%M:%S, %#d.%#m.%Y")

        embed = discord.Embed(
        description = f"{genre_info}",
        colour = 0x4a5fc3
        )

        embed.set_author(name=f"Genre info for {lastfm_username} about {genre_name}")
        embed.set_footer(text=f"Requested by {ctx.author.name}#{ctx.author.discriminator} • {timestamp}")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(genregetinfo(bot))