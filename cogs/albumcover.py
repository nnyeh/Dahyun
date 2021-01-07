import os
import pytz
import discord
import requests
from discord.ext import commands
from data import database as db
from datetime import datetime

class albumcover(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["co"])
    async def albumcover(self, ctx, *, arg=None):
        async with ctx.typing():
            
            username = db.get_user(ctx.author.id)

            if username is None:
                return await ctx.send(f"`You need to first set your Last.fm username with the command`\n```>set [your username]```")

            lastfm_username = username [0][1];
            if not lastfm_username:
                return await ctx.send(f"`You need to first set your Last.fm username with the command`\n```>set [your username]```")

            cet = pytz.timezone("CET")
            now = datetime.now(cet)
            timestamp = now.strftime("%#H:%M:%S, %#d.%#m.%Y")

            if arg is None:
                recent_tracks_params = {
                    "limit": "1",
                    "user": lastfm_username,
                    "api_key": os.getenv("LASTFM_API_KEY"),
                    "format": "json",
                    "method": "user.getRecentTracks"
                }

                r = requests.get("http://ws.audioscrobbler.com/2.0/", params=recent_tracks_params)
                rtdata = r.json()
                rtinfo = rtdata["recenttracks"]["track"][0]
                artist = rtinfo["artist"]["#text"]
                album = rtinfo["album"]["#text"]

                album_info_params = {
                    "artist": artist,
                    "album": album,
                    "autocorrect": "1",
                    "api_key": os.getenv("LASTFM_API_KEY"),
                    "format": "json",
                    "method": "album.getInfo"
                }

                r = requests.get("http://ws.audioscrobbler.com/2.0/", params=album_info_params)
                abidata = r.json()
            else:
                try:
                    artist, album = arg.split("|")
                except:
                    return await ctx.send(embed = discord.Embed(
                    description = "Use `|` to separate the artist and the album.",
                    colour = 0x4a5fc3
                    ))
                album_info_params = {
                    "artist": artist.strip(),
                    "album": album.strip(),
                    "autocorrect": "1",
                    "api_key": os.getenv("LASTFM_API_KEY"),
                    "format": "json",
                    "method": "album.getInfo"
                }

                r = requests.get("http://ws.audioscrobbler.com/2.0/", params=album_info_params)
                abidata = r.json()

            actual_artist = ""
            actual_album = ""
            album_url = ""
            album_cover = ""
            try:
                actual_artist = abidata["album"]["artist"]
                actual_album = abidata["album"]["name"]
                album_url = abidata["album"]["url"]
                album_cover = abidata["album"]["image"][-1]["#text"]
            except KeyError:
                embed = discord.Embed(description = f"**{actual_artist} - [{actual_album}]({album_url})**\n*No cover exists for this album.*", colour = 0x4a5fc3)
                embed.set_footer(text=f"Requested by {ctx.author.name}#{ctx.author.discriminator} • {timestamp} CET")
                return await ctx.send(embed=embed)

            if album_cover == "":
                embed = discord.Embed(description = f"**{actual_artist} - [{actual_album}]({album_url})**\n*No cover exists for this album.*", colour = 0x4a5fc3)
                embed.set_footer(text=f"Requested by {ctx.author.name}#{ctx.author.discriminator} • {timestamp} CET")
            else:
                embed = discord.Embed(description = f"**{actual_artist} - [{actual_album}]({album_url})**", colour = 0x4a5fc3)
                embed.set_image(url=f"{album_cover}")
            embed.set_footer(text=f"Requested by {ctx.author.name}#{ctx.author.discriminator} • {timestamp} CET")

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(albumcover(bot))