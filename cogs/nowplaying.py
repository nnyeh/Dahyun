import os
import discord
import asyncio
import requests
from discord.ext import commands
from data import database as db
from aiohttp import connector

class nowplaying(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["np"])
    async def nowplaying(self, ctx, arg=None):
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
                "limit": "1",
                "user": lastfm_username,
                "api_key": os.getenv("LASTFM_API_KEY"),
                "format": "json",
                "method": "user.getRecentTracks"
            }

            r1 = requests.get("http://ws.audioscrobbler.com/2.0/", params=recent_tracks_params)
            rtdata = r1.json()
            await asyncio.sleep(0.25)

            rtinfo = rtdata["recenttracks"]["track"][0]
            artist = rtinfo["artist"]["#text"]
            track = rtinfo["name"]
            album = rtinfo["album"]["#text"]
            image = rtinfo["image"][-1]["#text"]
            total_playcount = rtdata["recenttracks"]["@attr"]["total"]
            track_url = rtinfo["url"]

            np = "@attr" in rtinfo and "nowplaying" in rtinfo["@attr"]
            state = "Now playing for" if np else "Last scrobbled track for"

            artist_info_params = {
                "artist": artist,
                "user": lastfm_username,
                "api_key": os.getenv("LASTFM_API_KEY"),
                "format": "json",
                "method": "artist.getInfo"
            }

            r2 = requests.get("http://ws.audioscrobbler.com/2.0/", params=artist_info_params)
            aidata = r2.json()
            await asyncio.sleep(0.25)
            try:
                artist_playcount = aidata["artist"]["stats"]["userplaycount"]
            except KeyError:
                artist_playcount = "N/A"
            artist_url = aidata["artist"]["url"]
            artist_tags = [tag["name"] for tag in aidata["artist"]["tags"]["tag"]]
            artist_tags_string = " • ".join(artist_tags)

            album_info_params = {
                "artist": artist,
                "album": album,
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

            track_info_params = {
                "track": track,
                "artist": artist,
                "user": lastfm_username,
                "api_key": os.getenv("LASTFM_API_KEY"),
                "format": "json",
                "method": "track.getInfo"
            }

            r4 = requests.get("http://ws.audioscrobbler.com/2.0/", params=track_info_params)
            trackdata = r4.json()
            try:
                track_scrobbles = trackdata["track"]["userplaycount"] + " track scrobbles"
            except KeyError:
                track_scrobbles = "No data on Last.fm"

        if album == "":
            embed = discord.Embed(
                url = track_url,
                title = track,
                description = f"By **[{artist}]({artist_url})**",
                colour = 0x4a5fc3)
        else:
            embed = discord.Embed(
                url = track_url,
                title = track,
                description = f"By **[{artist}]({artist_url})** from **[{album}]({album_url})**",
                colour = 0x4a5fc3)

        embed.set_author(name=f"{state} {lastfm_username}", icon_url=pfp)
        embed.set_thumbnail(url=image)
        embed.set_footer(text=f"{artist_tags_string.lower()}\n{track_scrobbles} • {artist_playcount} {artist} scrobbles • {total_playcount} total scrobbles")

        try:
            await ctx.send(embed=embed)
        except connector.ClientConnectorError:
            await ctx.send(f"`Something went wrong! Try again.`")

def setup(bot):
    bot.add_cog(nowplaying(bot))