import os
import discord
import requests
import pyyoutube
from discord.ext import commands
from data import database as db
from datetime import datetime

class getyoutubelink(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["yt"])
    async def youtube(self, ctx, *, arg=None):

        now = datetime.now()
        timestamp = now.strftime("%#H:%M:%S, %#d.%#m.%Y")

        if arg is None:
            username = db.get_user(ctx.author.id)

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

            r = requests.get("http://ws.audioscrobbler.com/2.0/", params=recent_tracks_params)
            rtdata = r.json()
            rtinfo = rtdata["recenttracks"]["track"][0]
            artist = rtinfo["artist"]["#text"]
            track = rtinfo["name"]

            np = "@attr" in rtinfo and "nowplaying" in rtinfo["@attr"]
            state = f"*Now playing for {lastfm_username}*" if np else f"*Last scrobbled track for {lastfm_username}*"

            video_info_params = {
                "part": "snippet",
                "type": "video",
                "maxResults": 1,
                "q": f"{artist} {track}",
                "key": os.getenv("YOUTUBE_API_KEY"),
            }

            r = requests.get("https://www.googleapis.com/youtube/v3/search", params=video_info_params)
            vidata = r.json()
        else:
            artist, track = arg.split("|")
            video_info_params = {
                "part": "snippet",
                "type": "video",
                "maxResults": 1,
                "q": f"{artist} {track}",
                "key": os.getenv("YOUTUBE_API_KEY"),
            }

            r = requests.get("https://www.googleapis.com/youtube/v3/search", params=video_info_params)
            vidata = r.json()

            state = f"*Link requested by {ctx.author.name}#{ctx.author.discriminator}*"

        video_id = vidata["items"][0]["id"]["videoId"]
        video_url = f"https://youtube.com/watch?v={video_id}"

        await ctx.send(f"{state}\n{video_url}")

def setup(bot):
    bot.add_cog(getyoutubelink(bot))