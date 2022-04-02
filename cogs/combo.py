import os
import discord
import requests
import urllib.parse
from discord.ext import commands
from data import database as db
from datetime import datetime, timedelta

class combo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def combo(self, ctx, arg=None):
        async with ctx.typing():

            if arg is None:
                username = db.get_user(ctx.author.id)
                author = ctx.message.author
                pfp = author.avatar_url
            else:
                username = db.get_user(ctx.message.mentions[0].id)
                author = ctx.message.mentions[0]
                pfp = author.avatar_url

            if username is None:
                embed = discord.Embed(description = f"You need to first set your Last.fm username with the command\n`>set [your username]`", colour = 0x4a5fc3)
                return await ctx.send(embed=embed)

            lastfm_username = username [0][1];
            if not lastfm_username:
                embed = discord.Embed(description = f"You need to first set your Last.fm username with the command\n`>set [your username]`", colour = 0x4a5fc3)
                return await ctx.send(embed=embed)

            recent_tracks_params = {
                "limit": "1000",
                "user": lastfm_username,
                "api_key": os.getenv("LASTFM_API_KEY"),
                "format": "json",
                "method": "user.getRecentTracks"
            }

            r = requests.get("http://ws.audioscrobbler.com/2.0/", params=recent_tracks_params)
            rtdata = r.json()

            try:
                rtinfo = rtdata["recenttracks"]["track"][0]
            except IndexError:
                embed = discord.Embed(description = f"**You haven't listened to anything yet on Last.fm!**", colour = 0x4a5fc3)
                return await ctx.send(embed=embed)
            artist_name = rtinfo["artist"]["#text"]
            album_name = rtinfo["album"]["#text"]

            np = "@attr" in rtinfo and "nowplaying" in rtinfo["@attr"]

            album_info_params = {
                "artist": artist_name,
                "album": album_name,
                "user": lastfm_username,
                "api_key": os.getenv("LASTFM_API_KEY"),
                "format": "json",
                "method": "album.getInfo"
            }

            r3 = requests.get("http://ws.audioscrobbler.com/2.0/", params=album_info_params)
            abidata = r3.json()
            try:
                first_album_url = abidata["album"]["url"]
            except KeyError:
                first_album_url = ""

            first_artist_url = f"https://www.last.fm/music/" + urllib.parse.quote_plus(f"{artist_name}", safe="/")
            first_track_url = f"https://www.last.fm/music/" + urllib.parse.quote_plus(f"{artist_name}/{album_name}/{track}", safe="/")

            tracks = rtdata["recenttracks"]["track"]
            first_artist_obj = tracks[0]
            first_artist_name = first_artist_obj["artist"]["#text"]
            first_artist_name_lower = first_artist_obj["artist"]["#text"].lower()
            first_artist_album = first_artist_obj["album"]["#text"]
            first_artist_album_lower = first_artist_obj["album"]["#text"].lower()
            first_artist_track = first_artist_obj["name"]
            first_artist_track_lower = first_artist_obj["name"].lower()

            first_artist_combo = 0
            first_album_combo = 0
            first_track_combo = 0

            for track in tracks: 
                if (track["artist"]["#text"].lower() == first_artist_name_lower):
                    if 0 <= first_artist_combo < 1000:
                        first_artist_combo += 1
                else:
                    break

            for track in tracks: 
                if (track["album"]["#text"].lower() == first_artist_album_lower):
                    if 0 <= first_album_combo < 1000:
                        first_album_combo += 1
                else:
                    break

            for track in tracks: 
                if (track["name"].lower() == first_artist_track_lower):
                    if 0 <= first_track_combo < 1000:
                        first_track_combo += 1
                else:
                    break

            second_artist_combo = 0
            second_album_combo = 0
            second_track_combo = 0

            if first_artist_combo == 1000 or first_album_combo == 1000 or first_track_combo == 1000:
                recent_tracks_params = {
                "limit": "1000",
                "page": "2",
                "user": lastfm_username,
                "api_key": os.getenv("LASTFM_API_KEY"),
                "format": "json",
                "method": "user.getRecentTracks"
                }

                r = requests.get("http://ws.audioscrobbler.com/2.0/", params=recent_tracks_params)
                rtdata = r.json()

                rtinfo = rtdata["recenttracks"]["track"][0]
                artist_name = rtinfo["artist"]["#text"]
                album_name = rtinfo["album"]["#text"]

                tracks = rtdata["recenttracks"]["track"]

                if first_artist_combo == 1000:
                    for track in tracks: 
                        if (track["artist"]["#text"] == first_artist_name):
                            if 0 <= second_artist_combo < 1000:
                                second_artist_combo += 1
                        else:
                            break

                if first_album_combo == 1000:
                    for track in tracks: 
                        if (track["album"]["#text"] == first_artist_album):
                            if 0 <= second_album_combo < 1000:
                                second_album_combo += 1
                        else:
                            break

                if first_track_combo == 1000:
                    for track in tracks: 
                        if (track["name"] == first_artist_track):
                            if 0 <= second_track_combo < 1000:
                                second_track_combo += 1
                        else:
                            break

            third_artist_combo = 0
            third_album_combo = 0
            third_track_combo = 0

            if second_artist_combo == 1000 or second_album_combo == 1000 or second_track_combo == 1000:
                recent_tracks_params = {
                "limit": "1000",
                "page": "3",
                "user": lastfm_username,
                "api_key": os.getenv("LASTFM_API_KEY"),
                "format": "json",
                "method": "user.getRecentTracks"
                }

                r = requests.get("http://ws.audioscrobbler.com/2.0/", params=recent_tracks_params)
                rtdata = r.json()

                rtinfo = rtdata["recenttracks"]["track"][0]
                artist_name = rtinfo["artist"]["#text"]
                album_name = rtinfo["album"]["#text"]

                tracks = rtdata["recenttracks"]["track"]

                if second_artist_combo == 1000:
                    for track in tracks: 
                        if (track["artist"]["#text"] == first_artist_name):
                            if 0 <= third_artist_combo < 1000:
                                third_artist_combo += 1
                        else:
                            break

                if second_album_combo == 1000:
                    for track in tracks: 
                        if (track["album"]["#text"] == first_artist_album):
                            if 0 <= third_album_combo < 1000:
                                third_album_combo += 1
                        else:
                            break

                if second_track_combo == 1000:
                    for track in tracks: 
                        if (track["name"] == first_artist_track):
                            if 0 <= third_track_combo < 1000:
                                third_track_combo += 1
                        else:
                            break

            fourth_artist_combo = 0
            fourth_album_combo = 0
            fourth_track_combo = 0

            if third_artist_combo == 1000 or third_album_combo == 1000 or third_track_combo == 1000:
                recent_tracks_params = {
                "limit": "1000",
                "page": "4",
                "user": lastfm_username,
                "api_key": os.getenv("LASTFM_API_KEY"),
                "format": "json",
                "method": "user.getRecentTracks"
                }

                r = requests.get("http://ws.audioscrobbler.com/2.0/", params=recent_tracks_params)
                rtdata = r.json()

                rtinfo = rtdata["recenttracks"]["track"][0]
                artist_name = rtinfo["artist"]["#text"]
                album_name = rtinfo["album"]["#text"]

                tracks = rtdata["recenttracks"]["track"]

                if third_artist_combo == 1000:
                    for track in tracks: 
                        if (track["artist"]["#text"] == first_artist_name):
                            if 0 <= fourth_artist_combo < 1000:
                                fourth_artist_combo += 1
                        else:
                            break

                if third_album_combo == 1000:
                    for track in tracks: 
                        if (track["album"]["#text"] == first_artist_album):
                            if 0 <= fourth_album_combo < 1000:
                                fourth_album_combo += 1
                        else:
                            break

                if third_track_combo == 1000:
                    for track in tracks: 
                        if (track["name"] == first_artist_track):
                            if 0 <= fourth_track_combo < 1000:
                                fourth_track_combo += 1
                        else:
                            break

            fifth_artist_combo = 0
            fifth_album_combo = 0
            fifth_track_combo = 0

            if fourth_artist_combo == 1000 or fourth_album_combo == 1000 or fourth_track_combo == 1000:
                recent_tracks_params = {
                "limit": "1000",
                "page": "5",
                "user": lastfm_username,
                "api_key": os.getenv("LASTFM_API_KEY"),
                "format": "json",
                "method": "user.getRecentTracks"
                }

                r = requests.get("http://ws.audioscrobbler.com/2.0/", params=recent_tracks_params)
                rtdata = r.json()

                rtinfo = rtdata["recenttracks"]["track"][0]
                artist_name = rtinfo["artist"]["#text"]
                album_name = rtinfo["album"]["#text"]

                tracks = rtdata["recenttracks"]["track"]

                if fourth_artist_combo == 1000:
                    for track in tracks: 
                        if (track["artist"]["#text"] == first_artist_name):
                            if 0 <= fifth_artist_combo < 1000:
                                fifth_artist_combo += 1
                        else:
                            break

                if fourth_album_combo == 1000:
                    for track in tracks: 
                        if (track["album"]["#text"] == first_artist_album):
                            if 0 <= fifth_album_combo < 1000:
                                fifth_album_combo += 1
                        else:
                            break

                if fourth_track_combo == 1000:
                    for track in tracks: 
                        if (track["name"] == first_artist_track):
                            if 0 <= fifth_track_combo < 1000:
                                fifth_track_combo += 1
                        else:
                            break

            artist_combo_text = ""
            album_combo_text = ""
            track_combo_text = ""
            no_combo_text = ""
            add_artist_combos = first_artist_combo + second_artist_combo + third_artist_combo + fourth_artist_combo + fifth_artist_combo
            add_album_combos = first_album_combo + second_album_combo + third_album_combo + fourth_album_combo + fifth_album_combo
            add_track_combos = first_track_combo + second_track_combo + third_track_combo + fourth_track_combo + fifth_track_combo
            artist_combo = add_artist_combos if not np else (add_artist_combos - 1)
            album_combo = add_album_combos if not np else (add_album_combos - 1)
            track_combo = add_track_combos if not np else (add_track_combos - 1)

            if artist_combo >= 2:
                artist_combo_text = f"**Artist:** {artist_combo} plays in a row - **[{first_artist_name}]({first_artist_url})**\n"
            if album_combo >= 2 and first_album_url != "":
                    album_combo_text = f"**Album:** {album_combo} plays in a row - **[{first_artist_album}]({first_album_url})**\n"
            else:
                if album_combo >= 2 and first_album_url == "":
                    album_combo_text = f"**Album:** {album_combo} plays in a row - **{first_artist_album}**\n"
            if track_combo >= 2:
                track_combo_text = f"**Track:** {track_combo} plays in a row - **[{first_artist_track}]({first_track_url})**"
            if artist_combo_text == "" and album_combo_text == "" and track_combo_text == "":
                no_combo_text = f"*No consecutive tracks found.*"

            embed = discord.Embed(
            description = f"{no_combo_text}{artist_combo_text}{album_combo_text}{track_combo_text}",
            timestamp = datetime.now() - timedelta(hours=2),
            colour = 0x4a5fc3
            )

            embed.set_author(name=f"Active Combo for {lastfm_username}", icon_url=pfp)
            embed.set_footer(text=f"Requested by {ctx.author.name}#{ctx.author.discriminator}")

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(combo(bot))