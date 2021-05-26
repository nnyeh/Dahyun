import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import CommandNotFound

bot = commands.Bot(">", case_insensitive=True)

@bot.event
async def on_ready():
    print("Online")
    return await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="music"))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
ADMIN = os.getenv("ADMIN_ID")
APIKEY = os.getenv("LASTFM_API_KEY")
YTAPIKEY = os.getenv("YOUTUBE_API_KEY")

bot.remove_command("help")
bot.load_extension("cogs.albumcover")
bot.load_extension("cogs.albumgetinfo")
bot.load_extension("cogs.artistgetinfo")
bot.load_extension("cogs.combo")
bot.load_extension("cogs.genregetinfo")
bot.load_extension("cogs.getspotifylink")
bot.load_extension("cogs.getyoutubelink")
bot.load_extension("cogs.github")
bot.load_extension("cogs.help")
bot.load_extension("cogs.lyrics")
bot.load_extension("cogs.nowplaying")
bot.load_extension("cogs.profile")
bot.load_extension("cogs.setusername")
bot.load_extension("cogs.sunmutsis")
bot.load_extension("cogs.unsetusername")
bot.load_extension("cogs.usertopartists")
bot.load_extension("cogs.usertoptags")
bot.load_extension("cogs.whoknows")

bot.run(TOKEN)