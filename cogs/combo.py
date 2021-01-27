import os
import asyncio
import discord
import requests
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
                return await ctx.send(f"`You need to first set your Last.fm username with the command`\n```>set [your username]```")

            lastfm_username = username [0][1];
            if not lastfm_username:
                return await ctx.send(f"`You need to first set your Last.fm username with the command`\n```>set [your username]```")

            recent_tracks_params = {
                "limit": "1000",
                "user": lastfm_username,
                "api_key": os.getenv("LASTFM_API_KEY"),
                "format": "json",
                "method": "user.getRecentTracks"
            }

            r = requests.get("http://ws.audioscrobbler.com/2.0/", params=recent_tracks_params)
            rtdata = r.json()
            await asyncio.sleep(0.25)

            rtinfo = rtdata["recenttracks"]["track"][0]
            artist_name = rtinfo["artist"]["#text"]
            album_name = rtinfo["album"]["#text"]
            track_name = rtinfo["name"]
            track_url = rtinfo["url"]

            artist_info_params = {
                "artist": artist_name,
                "user": lastfm_username,
                "api_key": os.getenv("LASTFM_API_KEY"),
                "format": "json",
                "method": "artist.getInfo"
            }

            r2 = requests.get("http://ws.audioscrobbler.com/2.0/", params=artist_info_params)
            aidata = r2.json()
            await asyncio.sleep(0.25)
            artist_url = aidata["artist"]["url"]

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
            await asyncio.sleep(0.25)
            try:
                album_url = abidata["album"]["url"]
            except KeyError:
                album_url = ""
            tracks = rtdata["recenttracks"]["track"]
            first_artist_obj = tracks[0]
            first_artist_name = first_artist_obj["artist"]["#text"]
            first_artist_album = first_artist_obj["album"]["#text"]
            first_artist_track = first_artist_obj["name"]

            artist_combo = 0
            album_combo = 0
            track_combo = 0

            for track in tracks: 
                if (track["artist"]["#text"] == first_artist_name):
                    artist_combo += 1
                else:
                    break

            for track in tracks: 
                if (track["album"]["#text"] == first_artist_album):
                    album_combo += 1
                else:
                    break

            for track in tracks: 
                if (track["name"] == first_artist_track):
                    track_combo += 1
                else:
                    break

            artist_combo_text = ""
            album_combo_text = ""
            track_combo_text = ""
            no_combo_text = ""

            if artist_combo >= 2:
                artist_combo_text = f"**Artist:** {artist_combo} plays in a row - **[{artist_name}]({artist_url})**\n"
            if album_combo >= 2 and album_url != "":
                    album_combo_text = f"**Album:** {album_combo} plays in a row - **[{album_name}]({album_url})**\n"
            else:
                if album_combo >= 2 and album_url == "":
                    album_combo_text = f"**Album:** {album_combo} plays in a row - **{album_name}**\n"
            if track_combo >= 2:
                track_combo_text = f"**Track:** {track_combo} plays in a row - **[{track_name}]({track_url})**"
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