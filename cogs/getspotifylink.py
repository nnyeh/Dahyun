import os
import spotipy
import requests
from discord.ext import commands
from data import database as db
from spotipy.oauth2 import SpotifyClientCredentials

class getspotifylink(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["sp"])
    async def spotify(self, ctx, *, arg=None):

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
            track = rtinfo["name"]

            np = "@attr" in rtinfo and "nowplaying" in rtinfo["@attr"]
            state = f"*Now playing for {lastfm_username}*" if np else f"*Last scrobbled track for {lastfm_username}*"

            sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
            results = sp.search(track, type="track", limit=1)
            spotify_url = results["tracks"]["items"][0]["external_urls"]["spotify"]
        else:
            sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
            results = sp.search(arg, type="track", limit=1)
            spotify_url = results["tracks"]["items"][0]["external_urls"]["spotify"]

            state = f"*Link requested by {ctx.author.name}#{ctx.author.discriminator}*"

        await ctx.send(f"{state}\n{spotify_url}")

def setup(bot):
    bot.add_cog(getspotifylink(bot))