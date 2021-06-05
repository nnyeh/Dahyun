import os
import spotipy
import discord
import requests
from discord.ext import commands
from data import database as db
from datetime import datetime, timedelta
from spotipy.oauth2 import SpotifyClientCredentials

class albumcover(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["co"])
    async def albumcover(self, ctx, *, arg=None):
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
                    description = "Use the format `artist | album`.",
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

            actual_artist = abidata["album"]["artist"]
            actual_album = abidata["album"]["name"]
            api_album_cover = abidata["album"]["image"][-1]["#text"]
            no_file_type_album_cover = api_album_cover.rsplit(".",1)[0]
            higher_res_album_cover = no_file_type_album_cover.replace("300x300", "700x0", 1)

            
            try:
                album_url = abidata["album"]["url"]
            except KeyError:
                album_url = ""

            try:
                album_cover = abidata["album"]["image"][-1]["#text"]
            except KeyError:
                embed = discord.Embed(description = f"**{actual_artist} - [{actual_album}]({album_url})**\n\n*No cover exists for this album.*", timestamp = datetime.now() - timedelta(hours=2), colour = 0x4a5fc3)
                embed.set_footer(text=f"Requested by {ctx.author.name}#{ctx.author.discriminator}")

            if album_cover == "":
                embed = discord.Embed(description = f"**{actual_artist} - [{actual_album}]({album_url})**\n\n*No cover exists for this album.*", timestamp = datetime.now() - timedelta(hours=2), colour = 0x4a5fc3)
                embed.set_footer(text=f"Requested by {ctx.author.name}#{ctx.author.discriminator}")
            else:
                embed = discord.Embed(description = f"**{actual_artist} - [{actual_album}]({album_url})**", timestamp = datetime.now() - timedelta(hours=2), colour = 0x4a5fc3)
                embed.set_image(url=f"{higher_res_album_cover}")
            embed.set_footer(text=f"Requested by {ctx.author.name}#{ctx.author.discriminator}")

        await ctx.send(embed=embed)

    @commands.command(aliases=["sco"])
    async def albumcoverspotify(self, ctx, *, arg=None):
        async with ctx.typing():
            
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
                    "artist": artist.strip(),
                    "album": album.strip(),
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
                    description = "Use the format `artist | album`.",
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
            actual_artist = abidata["album"]["artist"]
            actual_album = abidata["album"]["name"]

            try:
                album_url = abidata["album"]["url"]
            except KeyError:
                album_url = ""

            sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
            sp_album_image = ""
            results = sp.search(f"{actual_artist} {actual_album}", type="track", limit=20)
            items = results["tracks"]["items"]
            lfm_artist_name_lowercase = f"{actual_artist.lower()}"
            lfm_album_name_lowercase = f"{actual_album.lower()}"

            for sp_track in items:
                sp_artist_correct = sp_track["artists"][0]
                sp_album_correct = sp_track["album"]
                sp_artist_name_lowercase = sp_artist_correct["name"].lower()
                sp_album_name_lowercase = sp_album_correct["name"].lower()
                if lfm_artist_name_lowercase == sp_artist_name_lowercase and lfm_album_name_lowercase == sp_album_name_lowercase:
                    try:
                        sp_album_image = sp_track["album"]["images"][0]["url"]
                    except IndexError:
                        sp_album_image = None
                    break

            if sp_album_image is None:
                embed = discord.Embed(description = f"**{actual_artist} - [{actual_album}]({album_url})**\n*No cover exists for this album.*", timestamp = datetime.now() - timedelta(hours=2), colour = 0x4a5fc3)
                embed.set_footer(text=f"Requested by {ctx.author.name}#{ctx.author.discriminator}")
            else:
                embed = discord.Embed(description = f"**{actual_artist} - [{actual_album}]({album_url})**", timestamp = datetime.now() - timedelta(hours=2), colour = 0x4a5fc3)
                embed.set_image(url=f"{sp_album_image}")
            embed.set_footer(text=f"Requested by {ctx.author.name}#{ctx.author.discriminator}")

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(albumcover(bot))