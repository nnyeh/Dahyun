import os
import spotipy
import asyncio
import discord
import requests
from discord.ext import commands
from data import database as db
from spotipy.oauth2 import SpotifyClientCredentials

class artistgetinfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["ai"])
    async def artistinfo(self, ctx, *, arg=None):
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
                actual_artist = rtinfo["artist"]["#text"]

                artist_info_params = {
                "artist": actual_artist,
                "api_key": os.getenv("LASTFM_API_KEY"),
                "format": "json",
                "method": "artist.getInfo"
                }

                r = requests.get("http://ws.audioscrobbler.com/2.0/", params=artist_info_params)
                aidata = r.json()
                artist_url = aidata["artist"]["url"]
                try:
                    artist_info = aidata["artist"]["bio"]["summary"]
                except TypeError:
                    artist_info = ""
                try:
                    artist_tags = [tag["name"] for tag in aidata["artist"]["tags"]["tag"]]
                except TypeError:
                    artist_tags = ""
                artist_tags_string = " ∙ ".join(artist_tags)

            else:
                artist_info_params = {
                "artist": arg,
                "api_key": os.getenv("LASTFM_API_KEY"),
                "format": "json",
                "method": "artist.getInfo"
                }
            
                r = requests.get("http://ws.audioscrobbler.com/2.0/", params=artist_info_params)
                aidata = r.json()
                await asyncio.sleep(0.25)
                try:
                    actual_artist = aidata["artist"]["name"]
                except KeyError:
                    return await ctx.send(embed = discord.Embed(
                        description = f"This artist doesn't exist.",
                        colour = 0x4a5fc3
                        ))
                artist_url = aidata["artist"]["url"]
                artist_info = aidata["artist"]["bio"]["summary"]
                try:
                    artist_tags = [tag["name"] for tag in aidata["artist"]["tags"]["tag"]]
                except TypeError:
                    artist_tags = ""
                artist_tags_string = " ∙ ".join(artist_tags)

            artist_info = artist_info.strip()
            sep = "<a"
            artist_info = artist_info.split(sep, 1)[0]
            if len(artist_info)>460:
                artist_info = artist_info[:460] + "..."

            sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
            sp_artist_image = ""
            results = sp.search(actual_artist, type="artist", limit=20)
            items = results["artists"]["items"]
            lfm_artist_name_lowercase = f"{actual_artist.lower()}"

            for sp_artist in items:
                sp_artist_name_lowercase = sp_artist["name"].lower()
                if lfm_artist_name_lowercase == sp_artist_name_lowercase:
                    try:
                        sp_artist_image = sp_artist["images"][0]["url"]
                    except IndexError:
                        sp_artist_image = None
                    break
            
            embed = discord.Embed(
            colour = 0x4a5fc3
            )

            embed.set_author(name=f"Artist info for {lastfm_username} about {actual_artist}")
            if sp_artist_image is not None:
                embed.set_thumbnail(url=f"{sp_artist_image}")
            if artist_info != "":
                embed.add_field(name=f"Summary", value=f"{artist_info}", inline=False)
            if artist_info == "":
                embed.add_field(name=f"Summary", value=f"*No summary exists for this artist.*", inline=False)
            if artist_url is not None:
                embed.add_field(name="\u200b", value=f"[Link to the site]({artist_url})")
            if artist_tags is not None:
                embed.set_footer(text=f"{artist_tags_string.lower()}")

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(artistgetinfo(bot))