import os
import asyncio
import discord
import requests
from discord.ext import commands
from data import database as db

class albumgetinfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["abi"])
    async def albuminfo(self, ctx, *, arg=None):
        async with ctx.typing():
            
            username = db.get_user(ctx.author.id)

            if username is None:
                embed = discord.Embed(description = f"You need to first set your Last.fm username with the command\n`>set [your username]`", colour = 0x4a5fc3)
                return await ctx.send(embed=embed)

            lastfm_username = username [0][1];
            if not lastfm_username:
                embed = discord.Embed(description = f"You need to first set your Last.fm username with the command\n`>set [your username]`", colour = 0x4a5fc3)
                return await ctx.send(embed=embed)

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
                await asyncio.sleep(0.25)
                rtinfo = rtdata["recenttracks"]["track"][0]
                album_cover = rtinfo["image"][-1]["#text"]
                actual_artist = rtinfo["artist"]["#text"]
                actual_album = rtinfo["album"]["#text"]

                album_info_params = {
                    "artist": actual_artist,
                    "album": actual_album,
                    "autocorrect": "1",
                    "api_key": os.getenv("LASTFM_API_KEY"),
                    "format": "json",
                    "method": "album.getInfo"
                }

                r = requests.get("http://ws.audioscrobbler.com/2.0/", params=album_info_params)
                abidata = r.json()
            else:
                artist, album = arg.split("|")
                params = {
                    "artist": artist.strip(),
                    "album": album.strip(),
                    "api_key": os.getenv("LASTFM_API_KEY"),
                    "format": "json",
                    "method": "album.getInfo"
                }

                r = requests.get("http://ws.audioscrobbler.com/2.0/", params=params)
                abidata = r.json()
                await asyncio.sleep(0.25)

            try:
                actual_artist = abidata["album"]["artist"]
            except KeyError:
                return await ctx.send(embed = discord.Embed(description = f"This artist's album doesn't exist.", colour = 0x4a5fc3))
            try:
                album_info = abidata["album"]["wiki"]["content"]
            except KeyError:
                album_info = ""


            actual_album = abidata["album"]["name"]
            album_url = abidata["album"]["url"]
            album_cover = abidata["album"]["image"][-1]["#text"]
            album_tags = [tag["name"] for tag in abidata["album"]["tags"]["tag"]]
            album_tags_string = " • ".join(album_tags)

            album_info = album_info.strip()
            sep = "<a"
            album_info = album_info.split(sep, 1)[0]
            if len(album_info)>800:
                album_info = album_info[:800] + "..."

            embed = discord.Embed(
            colour = 0x4a5fc3
            )

            embed.set_author(name=f"Album info for {lastfm_username} about {actual_artist} - {actual_album}")
            if album_cover is not None:
                embed.set_thumbnail(url=f"{album_cover}")
            if album_info != "":
                embed.add_field(name=f"Summary", value=f"{album_info}", inline=False)
            if album_info == "":
                embed.add_field(name=f"Summary", value=f"*No summary exists for this album.*", inline=False)
            if album_url is not None:
                embed.add_field(name="\u200b", value=f"[Link to the site]({album_url})")
            if album_tags is not None:
                embed.set_footer(text=f"{album_tags_string.lower()}")

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(albumgetinfo(bot))