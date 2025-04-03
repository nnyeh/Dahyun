import os
import spotipy
import discord
import requests
import itertools
import urllib.parse
from discord.ext import commands
from data import database as db
from spotipy.oauth2 import SpotifyClientCredentials
from datetime import datetime, timedelta


class whoknows(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["wk"])
    async def whoknows(self, ctx, *, arg=None):
        async with ctx.typing():

            username = db.get_user(ctx.author.id)
            if ctx.author.id == 202534850119335937:

                if arg is None:
                    username = db.get_user(ctx.author.id)

                    if username is None:
                        embed = discord.Embed(description = f"You need to first set your Last.fm username with the command\n`>set [your username]`", colour = 0x4a5fc3)
                        return await ctx.send(embed=embed)

                    lastfm_username = username [0][1];
                    if not lastfm_username:
                        embed = discord.Embed(description = f"You need to first set your Last.fm username with the command\n`>set [your username]`", colour = 0x4a5fc3)
                        return await ctx.send(embed=embed)

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
                    artistname = rtinfo["artist"]["#text"]

                    artist_info_params = {
                    "artist": artistname,
                    "api_key": os.getenv("LASTFM_API_KEY"),
                    "format": "json",
                    "method": "artist.getInfo"
                    }
            
                    r = requests.get("http://ws.audioscrobbler.com/2.0/", params=artist_info_params)
                    aidata = r.json()
                    artist_url = f"https://www.last.fm/music/" + urllib.parse.quote_plus(f"{artistname}", safe="/")
                else:
                    artist_info_params = {
                    "artist": arg,
                    "api_key": os.getenv("LASTFM_API_KEY"),
                    "format": "json",
                    "method": "artist.getInfo"
                    }
            
                    r = requests.get("http://ws.audioscrobbler.com/2.0/", params=artist_info_params)
                    aidata = r.json()
                    artistname = aidata["artist"]["name"]
                    artist_url = f"https://www.last.fm/music/" + urllib.parse.quote_plus(f"{artistname}", safe="/")

                sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
                sp_artist_image = ""
                results = sp.search(artistname, type="artist", limit=20)
                items = results["artists"]["items"]
                lfm_artist_name_lowercase = f"{artistname.lower()}"

                for sp_artist in items:
                    sp_artist_name_lowercase = sp_artist["name"].lower()
                    if lfm_artist_name_lowercase == sp_artist_name_lowercase:
                        try:
                            sp_artist_image = sp_artist["images"][0]["url"]
                        except IndexError:
                            sp_artist_image = None
                        break

                listeners_list = {}
                listens = ""
                lastfm_username_url = ""
                users = db.lfmquery()
                names = itertools.cycle(users)
                for _ in users:
                    next_name = next(names)
                    artist_info_params = {"artist": artistname, "user": next_name, "api_key": os.getenv("LASTFM_API_KEY"), "format": "json", "method": "artist.getInfo"}
                    r = requests.get("http://ws.audioscrobbler.com/2.0/", params=artist_info_params)
                    aidata = r.json()
                    lastfm_username = f"{next_name}"
                    lastfm_username_url = f"https://www.last.fm/user/{lastfm_username}"
                    try:
                        listens = int(aidata["artist"]["stats"]["userplaycount"])
                    except (KeyError, TypeError):
                        listens = 0
                    if listens == 0:
                        continue
                    else:
                        listeners_list[f"[{next_name}]({lastfm_username_url})"] = int(f"{listens}")
                listeners_list_sorted = dict(sorted(listeners_list.items(), key=lambda item: item[1], reverse=True))
                listeners_ranked = ""
                for position, (name, listens) in enumerate(listeners_list_sorted.items(), start=1):
                    listeners_ranked += (str(position) + ". " + name + " - **" + str(listens) + "** plays" + "\n")
            
                if listeners_ranked == "":
                    listeners_ranked = f"*No one in this server has listened to this artist.*"

                embed = discord.Embed(
                url = artist_url,
                title = f"Who knows {artistname} in {ctx.guild.name}",
                description = f"{listeners_ranked}",
                timestamp = datetime.now() - timedelta(hours=2),
                colour = 0x4a5fc3
                )
            
                if sp_artist_image is not None:
                    embed.set_thumbnail(url=f"{sp_artist_image}")
                embed.set_footer(text=f"Requested by {ctx.author.name}#{ctx.author.discriminator}")
                await ctx.send(embed=embed)
            else:
                await ctx.send("`Only Emsa can do this command :)`")

async def setup(bot):
    await bot.add_cog(whoknows(bot))