import os
import imageio
import discord
import spotipy
import requests
import urllib.parse
from discord.ext import commands
from data import database as db
from spotipy.oauth2 import SpotifyClientCredentials

class nowjamming(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["nj"])
    async def nowjamming(self, ctx, arg=None):
        async with ctx.typing():

            username = db.get_user(ctx.author.id)
            author = ctx.message.author
            pfp = author.avatar.url

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

            r1 = requests.get("http://ws.audioscrobbler.com/2.0/", params=recent_tracks_params)
            rtdata = r1.json()

            try:
                rtinfo = rtdata["recenttracks"]["track"][0]
            except IndexError:
                embed = discord.Embed(description = f"**You haven't listened to anything yet on Last.fm!**", colour = 0x4a5fc3)
                return await ctx.send(embed=embed)
            artist = rtinfo["artist"]["#text"]
            track = rtinfo["name"]
            album = rtinfo["album"]["#text"]
            api_album_cover = rtinfo["image"][-1]["#text"]
            no_file_type_album_cover = api_album_cover.rsplit(".",1)[0]
            higher_res_album_cover = no_file_type_album_cover.replace("300x300", "700x0", 1)
            track_url = f"https://www.last.fm/music/" + urllib.parse.quote_plus(f"{artist}/{album}/{track}", safe="/")
            artist_url = f"https://www.last.fm/music/" + urllib.parse.quote_plus(f"{artist}", safe="/")
            album_url = f"https://www.last.fm/music/" + urllib.parse.quote_plus(f"{artist}/{album}", safe="/")

            track_info_params = {
                "track": track,
                "artist": artist,
                "user": lastfm_username,
                "api_key": os.getenv("LASTFM_API_KEY"),
                "format": "json",
                "method": "track.getInfo"
            }

            r2 = requests.get("http://ws.audioscrobbler.com/2.0/", params=track_info_params)
            rtdata = r2.json()
            
            try:
                loved = rtdata["track"]["userloved"]
                if loved is "1":
                    loved = "❤️ "
                else:
                    loved = ""
            except KeyError:
                loved = ""

            np = "@attr" in rtinfo and "nowplaying" in rtinfo["@attr"]
            state = "Now playing for" if np else "Last scrobbled track for"

            sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
            sp_track_id = ""
            results = sp.search(f"{track} {artist}", type="track", limit=20)
            items = results["tracks"]["items"]
            lfm_artist_name_lowercase = f"{artist.lower()}"

            for sp_track in items:
                sp_track_correct = sp_track["artists"][0]
                sp_artist_name_lowercase = sp_track_correct["name"].lower()
                if lfm_artist_name_lowercase == sp_artist_name_lowercase:
                    sp_track_id = items[0]["id"]
                    break

            sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
            results = sp.audio_features(tracks = (f"{sp_track_id}"))
            bpm = results[0]["tempo"]

        embed = discord.Embed(
            url = track_url,
            title = track,
            description = f"By **[{artist}]({artist_url})** from **[{album}]({album_url})**",
            colour = 0x4a5fc3)

        gif = discord.File("./gifs/catjam.gif", filename="gif.gif")

        embed.set_author(name=f"{loved}{state} {lastfm_username}", url=f"https://www.last.fm/user/{lastfm_username}", icon_url=pfp)
        embed.set_thumbnail(url=higher_res_album_cover)
        embed.set_image(url="attachment://gif.gif")

        await ctx.send(file=gif, embed=embed)

def setup(bot):
    bot.add_cog(nowjamming(bot))