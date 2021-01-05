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
            print(track)
            print("-----------")
            artist = rtinfo["artist"]["#text"]

            np = "@attr" in rtinfo and "nowplaying" in rtinfo["@attr"]
            state = f"*Now playing for {lastfm_username}*" if np else f"*Last scrobbled track for {lastfm_username}*"

            sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
            sp_track_url = ""
            results = sp.search(f"{track} {artist}", type="track", limit=50)
            items = results["tracks"]["items"]
            lfm_artist_name_lowercase = f"{artist.lower()}"

            for sp_track in items:
                sp_track_correct = sp_track["artists"][0]
                sp_artist_name_lowercase = sp_track_correct["name"].lower()
                print(sp_artist_name_lowercase)
                print(lfm_artist_name_lowercase)
                if lfm_artist_name_lowercase == sp_artist_name_lowercase:
                    sp_track_url = sp_track["external_urls"]["spotify"]
                    break
            
            print("------------------------")
        else:
            sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
            results = sp.search(arg, type="track", limit=1)
            sp_track_url = results["tracks"]["items"][0]["external_urls"]["spotify"]

            state = f"*Link requested by {ctx.author.name}#{ctx.author.discriminator}*"

        await ctx.send(f"{state}\n{sp_track_url}")

def setup(bot):
    bot.add_cog(getspotifylink(bot))