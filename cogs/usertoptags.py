import os
import random
import discord
import requests
from discord.ext import commands
from data import database as db
from datetime import datetime

class usertoptags(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["tt"])
    async def toptags(self, ctx, *, arg=None):

        valid_timeframes = ["w", "m", "q", "s", "y", "a", None]
        timeframe = ""
        if arg == "w":
            arg = "7day"
            timeframe = "of the last week"
        elif arg == "m":
            arg = "1month"
            timeframe = "of the last month"
        elif arg == "q":
            arg = "3month"
            timeframe = "of the last quarter"
        elif arg == "s":
            arg = "6month"
            timeframe = "of the last semester"
        elif arg == "y":
            arg = "12month"
            timeframe = "of the last year"
        elif arg == "a":
            arg = "overall"
            timeframe = "overall"
        elif arg is None:
            arg = "7day"
            timeframe = "of the last week"
        elif arg is not valid_timeframes:
            await ctx.send(f"`Invalid timeframe` <a:DubuAngry:773329674679746610>")
            return
            
            

        
        username = db.get_user(ctx.author.id)
        author = ctx.message.author
        pfp = author.avatar_url
        if username is None:
            return await ctx.send(f"`You need to first set your Last.fm username with the command`\n```>set [your username]```")

        lastfm_username = username [0][1];
        if not lastfm_username:
            return await ctx.send(f"`You need to first set your Last.fm username with the command`\n```>set [your username]```")

        top_artists_params = {
            "period": arg,
            "limit": "10",
            "user": lastfm_username,
            "api_key": os.getenv("API_KEY"),
            "format": "json",
            "method": "user.getTopArtists"
        }

        r = requests.get("http://ws.audioscrobbler.com/2.0/", params=top_artists_params)
        tadata = r.json()
        top_artists_names = [name["name"] for name in tadata["topartists"]["artist"]]
        first_top_artist = top_artists_names [0];
        second_top_artist = top_artists_names [1];
        third_top_artist = top_artists_names [2];
        fourth_top_artist = top_artists_names [3];
        fifth_top_artist = top_artists_names [4];
        sixth_top_artist = top_artists_names [5];
        seventh_top_artist = top_artists_names [6];
        eighth_top_artist = top_artists_names [7];
        ninth_top_artist = top_artists_names [8];
        tenth_top_artist = top_artists_names [9];

        artist_info_params = {
            "artist": first_top_artist,
            "user": lastfm_username,
            "api_key": os.getenv("API_KEY"),
            "format": "json",
            "method": "artist.getInfo"
        }

        r = requests.get("http://ws.audioscrobbler.com/2.0/", params=artist_info_params)
        aidata = r.json()
        try:
            first_artist_tags = [tag["name"] for tag in aidata["artist"]["tags"]["tag"]]
        except KeyError:
            first_artist_tags = [""]

        artist_info_params = {
            "artist": second_top_artist,
            "user": lastfm_username,
            "api_key": os.getenv("API_KEY"),
            "format": "json",
            "method": "artist.getInfo"
        }

        r = requests.get("http://ws.audioscrobbler.com/2.0/", params=artist_info_params)
        aidata = r.json()
        try:
            second_artist_tags = [tag["name"] for tag in aidata["artist"]["tags"]["tag"]]
        except KeyError:
            second_artist_tags = [""]

        artist_info_params = {
            "artist": third_top_artist,
            "user": lastfm_username,
            "api_key": os.getenv("API_KEY"),
            "format": "json",
            "method": "artist.getInfo"
        }

        r = requests.get("http://ws.audioscrobbler.com/2.0/", params=artist_info_params)
        aidata = r.json()
        try:
            third_artist_tags = [tag["name"] for tag in aidata["artist"]["tags"]["tag"]]
        except KeyError:
            third_artist_tags = [""]

        artist_info_params = {
            "artist": fourth_top_artist,
            "user": lastfm_username,
            "api_key": os.getenv("API_KEY"),
            "format": "json",
            "method": "artist.getInfo"
        }

        r = requests.get("http://ws.audioscrobbler.com/2.0/", params=artist_info_params)
        aidata = r.json()
        try:
            fourth_artist_tags = [tag["name"] for tag in aidata["artist"]["tags"]["tag"]]
        except KeyError:
            fourth_artist_tags = [""]

        artist_info_params = {
            "artist": fifth_top_artist,
            "user": lastfm_username,
            "api_key": os.getenv("API_KEY"),
            "format": "json",
            "method": "artist.getInfo"
        }

        r = requests.get("http://ws.audioscrobbler.com/2.0/", params=artist_info_params)
        aidata = r.json()
        try:
            fifth_artist_tags = [tag["name"] for tag in aidata["artist"]["tags"]["tag"]]
        except KeyError:
            fifth_artist_tags = [""]

        artist_info_params = {
            "artist": sixth_top_artist,
            "user": lastfm_username,
            "api_key": os.getenv("API_KEY"),
            "format": "json",
            "method": "artist.getInfo"
        }

        r = requests.get("http://ws.audioscrobbler.com/2.0/", params=artist_info_params)
        aidata = r.json()
        try:
            sixth_artist_tags = [tag["name"] for tag in aidata["artist"]["tags"]["tag"]]
        except KeyError:
            sixth_artist_tags = [""]

        artist_info_params = {
            "artist": seventh_top_artist,
            "user": lastfm_username,
            "api_key": os.getenv("API_KEY"),
            "format": "json",
            "method": "artist.getInfo"
        }

        r = requests.get("http://ws.audioscrobbler.com/2.0/", params=artist_info_params)
        aidata = r.json()
        try:
            seventh_artist_tags = [tag["name"] for tag in aidata["artist"]["tags"]["tag"]]
        except KeyError:
            seventh_artist_tags = [""]

        artist_info_params = {
            "artist": eighth_top_artist,
            "user": lastfm_username,
            "api_key": os.getenv("API_KEY"),
            "format": "json",
            "method": "artist.getInfo"
        }

        r = requests.get("http://ws.audioscrobbler.com/2.0/", params=artist_info_params)
        aidata = r.json()
        try:
            eighth_artist_tags = [tag["name"] for tag in aidata["artist"]["tags"]["tag"]]
        except KeyError:
            eighth_artist_tags = [""]

        artist_info_params = {
            "artist": ninth_top_artist,
            "user": lastfm_username,
            "api_key": os.getenv("API_KEY"),
            "format": "json",
            "method": "artist.getInfo"
        }

        r = requests.get("http://ws.audioscrobbler.com/2.0/", params=artist_info_params)
        aidata = r.json()
        try:
            ninth_artist_tags = [tag["name"] for tag in aidata["artist"]["tags"]["tag"]]
        except KeyError:
            ninth_artist_tags = [""]

        artist_info_params = {
            "artist": tenth_top_artist,
            "user": lastfm_username,
            "api_key": os.getenv("API_KEY"),
            "format": "json",
            "method": "artist.getInfo"
        }

        r = requests.get("http://ws.audioscrobbler.com/2.0/", params=artist_info_params)
        aidata = r.json()
        try:
            tenth_artist_tags = [tag["name"] for tag in aidata["artist"]["tags"]["tag"]]
        except KeyError:
            tenth_artist_tags = [""]

        all_artist_tags = first_artist_tags + second_artist_tags + third_artist_tags + fourth_artist_tags + fifth_artist_tags + sixth_artist_tags + seventh_artist_tags + eighth_artist_tags + ninth_artist_tags + tenth_artist_tags
        random.shuffle(all_artist_tags)
        no_duplicates = set(all_artist_tags)
        all_artist_tags_string = " • ".join(no_duplicates)
        

        now = datetime.now()
        timestamp = now.strftime("%#H:%M:%S, %#d.%#m.%Y")
        
        embed = discord.Embed(
            description = f"{all_artist_tags_string.lower()}",
            colour = 0x4a5fc3
        )

        embed.set_author(name=f"Top tags {timeframe} for {lastfm_username}", icon_url=pfp)
        embed.set_footer(text=f"Requested by {ctx.author.name}#{ctx.author.discriminator} • {timestamp}")

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(usertoptags(bot))