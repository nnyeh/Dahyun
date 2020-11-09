import os
from discord.ext import commands
import discord
from dotenv import load_dotenv
from data import database as db

bot = commands.Bot(">")

@bot.event
async def on_ready():
    print("Online")
    return await bot.change_presence(activity=discord.Activity(type=1))

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
ADMIN = os.getenv("ADMIN_ID")
APIKEY = os.getenv("API_KEY")

bot.remove_command("help")
bot.load_extension("cogs.albumcover")
bot.load_extension("cogs.albumgetinfo")
bot.load_extension("cogs.artistgetinfo")
bot.load_extension("cogs.combo")
bot.load_extension("cogs.help")
bot.load_extension("cogs.nowplaying")
bot.load_extension("cogs.profile")
bot.load_extension("cogs.setusername")
bot.load_extension("cogs.unsetusername")
bot.load_extension("cogs.usertopartists")
bot.load_extension("cogs.usertoptags")

bot.run(TOKEN)