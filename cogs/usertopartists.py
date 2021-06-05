import os
import asyncio
import discord
import requests
from discord.ext import commands
from data import database as db
from datetime import datetime, timedelta

class usertopartists(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["ta"])
    async def topartists(self, ctx, *, arg=None):
        async with ctx.typing():

            valid_timeframes = ["w", "m", "q", "s", "y", "a", None]
            timeframe = ""
            if arg is "w":
                arg = "7day"
                timeframe = "of the last week"
            elif arg is "m":
                arg = "1month"
                timeframe = "of the last month"
            elif arg is "q":
                arg = "3month"
                timeframe = "of the last quarter"
            elif arg is "s":
                arg = "6month"
                timeframe = "of the last semester"
            elif arg is "y":
                arg = "12month"
                timeframe = "of the last year"
            elif arg is "a":
                arg = "overall"
                timeframe = "overall"
            elif arg is None:
                arg = "7day"
                timeframe = "of the last week"
            elif arg is not valid_timeframes:
                await ctx.send(f"`Invalid timeframe` <a:DubuAngry:773329674679746610>")
                return
            
            username = db.get_user(ctx.author.id)
            author = ctx.message.author
            pfp = author.avatar_url
            if username is None:
                embed = discord.Embed(description = f"You need to first set your Last.fm username with the command\n`>set [your username]`", colour = 0x4a5fc3)
                return await ctx.send(embed=embed)

            lastfm_username = username [0][1];
            if not lastfm_username:
                embed = discord.Embed(description = f"You need to first set your Last.fm username with the command\n`>set [your username]`", colour = 0x4a5fc3)
                return await ctx.send(embed=embed)

            top_artists_params = {
                "period": arg,
                "limit": "10",
                "user": lastfm_username,
                "api_key": os.getenv("LASTFM_API_KEY"),
                "format": "json",
                "method": "user.getTopArtists"
            }

            r = requests.get("http://ws.audioscrobbler.com/2.0/", params=top_artists_params)
            tadata = r.json()
            await asyncio.sleep(0.25)
            top_artists_names = [name["name"] for name in tadata["topartists"]["artist"]]
            top_artists_string = "\n".join(top_artists_names)
            
            embed = discord.Embed(
                description = f"**{top_artists_string}**",
                timestamp = datetime.now() - timedelta(hours=2),
                colour = 0x4a5fc3
            )

            embed.set_author(name=f"Top artists {timeframe} for {lastfm_username}", icon_url=pfp)
            embed.set_footer(text=f"Requested by {ctx.author.name}#{ctx.author.discriminator}")

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(usertopartists(bot))