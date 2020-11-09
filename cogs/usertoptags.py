import os
import re
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

        if arg is "w":
            arg = "7day"
            timeframe = "of the last week"
        elif arg is "m":
            arg = "1month"
            timeframe = "of the last month"
        elif arg is "q":
            arg = "3month"
            timeframe = "of the last quarter"
        elif arg is "s":
            arg = "6month"
            timeframe = "of the last semester"
        elif arg is "y":
            arg = "12month"
            timeframe = "of the last year"
        elif arg is "a":
            arg = "overall"
            timeframe = "overall"
        elif arg is None:
            arg = "7day"
            timeframe = "of the last week"
        
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
        first_artist_tags = [tag["name"] for tag in aidata["artist"]["tags"]["tag"]]

        artist_info_params = {
            "artist": second_top_artist,
            "user": lastfm_username,
            "api_key": os.getenv("API_KEY"),
            "format": "json",
            "method": "artist.getInfo"
        }

        r = requests.get("http://ws.audioscrobbler.com/2.0/", params=artist_info_params)
        aidata = r.json()
        second_artist_tags = [tag["name"] for tag in aidata["artist"]["tags"]["tag"]]

        artist_info_params = {
            "artist": third_top_artist,
            "user": lastfm_username,
            "api_key": os.getenv("API_KEY"),
            "format": "json",
            "method": "artist.getInfo"
        }

        r = requests.get("http://ws.audioscrobbler.com/2.0/", params=artist_info_params)
        aidata = r.json()
        third_artist_tags = [tag["name"] for tag in aidata["artist"]["tags"]["tag"]]

        artist_info_params = {
            "artist": fourth_top_artist,
            "user": lastfm_username,
            "api_key": os.getenv("API_KEY"),
            "format": "json",
            "method": "artist.getInfo"
        }

        r = requests.get("http://ws.audioscrobbler.com/2.0/", params=artist_info_params)
        aidata = r.json()
        fourth_artist_tags = [tag["name"] for tag in aidata["artist"]["tags"]["tag"]]
        
        artist_info_params = {
            "artist": fifth_top_artist,
            "user": lastfm_username,
            "api_key": os.getenv("API_KEY"),
            "format": "json",
            "method": "artist.getInfo"
        }

        r = requests.get("http://ws.audioscrobbler.com/2.0/", params=artist_info_params)
        aidata = r.json()
        fifth_artist_tags = [tag["name"] for tag in aidata["artist"]["tags"]["tag"]]
        
        artist_info_params = {
            "artist": sixth_top_artist,
            "user": lastfm_username,
            "api_key": os.getenv("API_KEY"),
            "format": "json",
            "method": "artist.getInfo"
        }

        r = requests.get("http://ws.audioscrobbler.com/2.0/", params=artist_info_params)
        aidata = r.json()
        sixth_artist_tags = [tag["name"] for tag in aidata["artist"]["tags"]["tag"]]
        
        artist_info_params = {
            "artist": seventh_top_artist,
            "user": lastfm_username,
            "api_key": os.getenv("API_KEY"),
            "format": "json",
            "method": "artist.getInfo"
        }

        r = requests.get("http://ws.audioscrobbler.com/2.0/", params=artist_info_params)
        aidata = r.json()
        seventh_artist_tags = [tag["name"] for tag in aidata["artist"]["tags"]["tag"]]
        
        artist_info_params = {
            "artist": eighth_top_artist,
            "user": lastfm_username,
            "api_key": os.getenv("API_KEY"),
            "format": "json",
            "method": "artist.getInfo"
        }

        r = requests.get("http://ws.audioscrobbler.com/2.0/", params=artist_info_params)
        aidata = r.json()
        eighth_artist_tags = [tag["name"] for tag in aidata["artist"]["tags"]["tag"]]
        
        artist_info_params = {
            "artist": ninth_top_artist,
            "user": lastfm_username,
            "api_key": os.getenv("API_KEY"),
            "format": "json",
            "method": "artist.getInfo"
        }

        r = requests.get("http://ws.audioscrobbler.com/2.0/", params=artist_info_params)
        aidata = r.json()
        ninth_artist_tags = [tag["name"] for tag in aidata["artist"]["tags"]["tag"]]

        artist_info_params = {
            "artist": tenth_top_artist,
            "user": lastfm_username,
            "api_key": os.getenv("API_KEY"),
            "format": "json",
            "method": "artist.getInfo"
        }

        r = requests.get("http://ws.audioscrobbler.com/2.0/", params=artist_info_params)
        aidata = r.json()
        tenth_artist_tags = [tag["name"] for tag in aidata["artist"]["tags"]["tag"]]

        all_artist_tags = first_artist_tags + second_artist_tags + third_artist_tags + fourth_artist_tags + fifth_artist_tags + sixth_artist_tags + seventh_artist_tags + eighth_artist_tags + ninth_artist_tags + tenth_artist_tags
        random.shuffle(all_artist_tags)
        no_duplicates = set(all_artist_tags)
        tags_string = " ".join(no_duplicates)
        no_best_of = (tags_string.replace("best of ", ""))
        remove_numbers = re.sub(r"[0-9]+ ", "", no_best_of)
        tags_list = list(remove_numbers.split(" "))
        all_artist_tags_string = " • ".join(tags_list)

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