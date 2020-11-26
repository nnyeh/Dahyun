import discord
from discord.ext import commands
# discord.errors.Forbidden: 403 Forbidden (error code: 50007): Cannot send messages to this user

class help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        
        embed = discord.Embed(
            title = "Commands",
            description = f"With some commands you can specify the member of whose data you want to return with a mention. You can also specify the artist and/or album with **[artist] | [album]** with some commands but if you do not specify them and you have your Last.fm username set on the server, it will return the data of whatever you're currently listening to.\n\nSome commands can be specified to use a different time frame:\n**w: week**\n**m: month**\n**q: quarter**\n**s: semester**\n**y: year**\n**a: alltime**\nIf no timeframe is specified, it defaults to a week.\n\n**>albumcover** or **>co** - Returns the album cover.\n**>albuminfo** or **>abi** - Returns the album info.\n**>artistinfo** or **>ai** - Returns the artist info.\n**>combo** - Displays the amount of plays of the same artist, album or song.\n**>genreinfo** or **>gi** - Returns info about a specified genre.\n**>youtube** or **>yt** - Returns a YouTube link of either a specified song or of your current/last scrobble.\n**>nowplaying** or **>np** - Returns your current songs info.\n**>profile** - Returns a link to the Last.fm profile.\n**>set** and **>unset** - Sets and unsets your username.\n**>topartists** or **>ta** - Returns the top artists of the specified timeframe.",
            colour = 0x4a5fc3
        )

        await ctx.author.send(embed=embed)

def setup(bot):
    bot.add_cog(help(bot))