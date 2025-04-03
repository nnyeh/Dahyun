import asyncio
import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import CommandNotFound

# Load environment variables first
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
ADMIN = os.getenv("ADMIN_ID")
APIKEY = os.getenv("LASTFM_API_KEY")
YTAPIKEY = os.getenv("YOUTUBE_API_KEY")

# Set up intents and create bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=">", intents=intents, case_insensitive=True)

@bot.event
async def on_ready():
    clear = lambda: os.system("cls")
    clear()
    print("Online")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="music"))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error

# Remove the help command before loading extensions
bot.remove_command("help")

# Load all extensions
async def setup_hook():
    extensions = [
        "cogs.albumcover",
        "cogs.albumgetinfo", 
        "cogs.artistgetinfo",
        "cogs.combo",
        "cogs.genregetinfo",
        "cogs.getspotifylink",
        "cogs.getyoutubelink",
        "cogs.github",
        "cogs.help",
        "cogs.lyrics",
        "cogs.nowplaying",
        "cogs.profile",
        "cogs.setusername",
        "cogs.sunmutsis",
        "cogs.unsetusername",
        "cogs.usertopartists",
        "cogs.usertoptags",
        "cogs.whoknows"
    ]
    
    for extension in extensions:
        try:
            await bot.load_extension(extension)
            print(f"Loaded {extension}")
        except Exception as e:
            print(f"Failed to load extension {extension}: {e}")

# Add the setup hook to the bot
bot.setup_hook = setup_hook

# Run the bot
async def main():
    try:
        await bot.start(TOKEN)
    except KeyboardInterrupt:
        await bot.close()

if __name__ == "__main__":
    asyncio.run(main())