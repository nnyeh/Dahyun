import os
import discord
import requests
from discord.ext import commands
from data import database as db

class albumcover(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["co"])
    async def albumcover(self, ctx, *, arg=None):

        username = db.get_user(ctx.author.id)

        if username is None:
            return await ctx.send(f"`You need to first set your Last.fm username with the command`\n```>set [your username]```")

        lastfm_username = username [0][1];
        if not lastfm_username:
            return await ctx.send(f"`You need to first set your Last.fm username with the command`\n```>set [your username]```")

        if arg is None:
            recent_tracks_params = {
                "limit": "1",
                "user": lastfm_username,
                "api_key": os.getenv("API_KEY"),
                "format": "json",
                "method": "user.getRecentTracks"
            }

            r = requests.get("http://ws.audioscrobbler.com/2.0/", params=recent_tracks_params)
            rtdata = r.json()
            rtinfo = rtdata["recenttracks"]["track"][0]
            album_cover = rtinfo["image"][-1]["#text"]
            artist = rtinfo["artist"]["#text"]
            album = rtinfo["album"]["#text"]

            album_info_params = {
                "artist": artist,
                "album": album,
                "autocorrect": "1",
                "api_key": os.getenv("API_KEY"),
                "format": "json",
                "method": "album.getInfo"
            }

            r = requests.get("http://ws.audioscrobbler.com/2.0/", params=album_info_params)
            abidata = r.json()
            album_url = abidata["album"]["url"]

            embed = discord.Embed(
            description = f"**{artist} - [{album}]({album_url})**",
            colour = 0x4a5fc3
            )

            embed.set_image(url=f"{album_cover}")
            embed.set_footer(text=f"Album cover requested by {ctx.author.name}#{ctx.author.discriminator}")

            await ctx.send(embed=embed)
        else:
            artist, album = arg.split("|")
            album_info_params = {
                "artist": artist.strip(),
                "album": album.strip(),
                "autocorrect": "1",
                "api_key": os.getenv("API_KEY"),
                "format": "json",
                "method": "album.getInfo"
            }

            r = requests.get("http://ws.audioscrobbler.com/2.0/", params=album_info_params)
            abidata = r.json()
            actual_artist = abidata["album"]["artist"]
            actual_album = abidata["album"]["name"]
            album_url = abidata["album"]["url"]
            album_cover = abidata["album"]["image"][-1]["#text"]

            embed = discord.Embed(
            description = f"**{actual_artist} - [{actual_album}]({album_url})**",
            colour = 0x4a5fc3
            )

            embed.set_image(url=f"{album_cover}")
            embed.set_footer(text=f"Album cover requested by {ctx.author.name}#{ctx.author.discriminator}")

            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(albumcover(bot))