import os
import discord
import requests
import lyricsgenius as lg
from discord.ext import commands
from data import database as db

class lyrics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def lyrics(self, ctx, arg=None):
        async with ctx.typing():

            username = db.get_user(ctx.author.id)

            if username is None:
                embed = discord.Embed(description = f"You need to first set your Last.fm username with the command\n**>set [your username]**", colour = 0x4a5fc3)
                return await ctx.send(embed=embed)

            lastfm_username = username [0][1];
            if not lastfm_username:
                embed = discord.Embed(description = f"You need to first set your Last.fm username with the command\n**>set [your username]**", colour = 0x4a5fc3)
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

            try:
                rtinfo = rtdata["recenttracks"]["track"][0]
            except IndexError:
                embed = discord.Embed(description = f"**You haven't listened to anything yet on Last.fm!**", colour = 0x4a5fc3)
                return await ctx.send(embed=embed)
            artist = rtinfo["artist"]["#text"]
            track = rtinfo["name"]

            genius = lg.Genius(skip_non_songs=True, verbose=False)
            song = genius.search_song(track, artist)
            try:
                lyrics = song.lyrics
            except AttributeError:
                lyrics = "*No lyrics were found.*"
            lyrics1 = lyrics[0:2000]

            if len(lyrics+track+artist)>2000:
                lyrics2 = lyrics[2000:4000]
                embed2 = discord.Embed(description = lyrics2, colour = 0x4a5fc3)
            if len(lyrics)>4000:
                lyrics3 = lyrics[4000:6000]
                lyrics2 = lyrics[2000:4000]
                embed3 = discord.Embed(description = lyrics3, colour = 0x4a5fc3)
            if len(lyrics)>6000:
                lyrics4 = lyrics[6000:8000]
                lyrics3 = lyrics[4000:6000]
                embed4 = discord.Embed(description = lyrics4, colour = 0x4a5fc3)

            embed1 = discord.Embed(
            title = f"Lyrics for {track} by {artist}",
            description = lyrics1,
            colour = 0x4a5fc3)

            await ctx.send(embed=embed1)
            if len(lyrics+track+artist)>2000:
                await ctx.send(embed=embed2)
                if len(lyrics)>4000:
                    await ctx.send(embed=embed3)
                    if len(lyrics)>6000:
                        await ctx.send(embed=embed4)         

def setup(bot):
    bot.add_cog(lyrics(bot))