import discord
from discord.ext import commands

class help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        
        embed = discord.Embed(
            title = "Commands",
            description = f"With some commands you can specify the member of whose data you want to return with a mention. You can also specify the artist and/or album with **[artist] | [album]** with some commands but if you do not specify them and you have your Last.fm username set on the server, it will return the data of whatever you're currently listening to.", value=f"Some commands can be specified to use a different time frame:\n**w: week**\n**m: month**\n**q: quarter**\n**s: semester**\n**y: year**\n**a: alltime**\nIf no timeframe is specified, it defaults to a week.",
            colour = 0x4a5fc3
        )

        embed.add_field(name=f"**>albumcover** or **>co**", value=f"Returns the album cover from Last.fm.", inline=False)
        embed.add_field(name=f"**>albumcoverspotify** or **>sco**", value=f"Returns the album cover from Spotify.", inline=False)
        embed.add_field(name=f"**>albuminfo** or **>abi**", value=f"Returns the album info.", inline=False)
        embed.add_field(name=f"**>artistinfo** or **>ai**", value=f"Returns the artist info.", inline=False)
        embed.add_field(name=f"**>combo**", value=f"Displays the amount of plays of the same artist, album or song.", inline=False)
        embed.add_field(name=f"**>genreinfo** or **>gi**", value=f"Returns info about a specified genre.", inline=False)
        embed.add_field(name=f"**>spotify** or **>sp**", value=f"Returns a Spotify link.", inline=False)
        embed.add_field(name=f"**>youtube** or **>yt**", value=f"Returns a YouTube link.", inline=False)
        embed.add_field(name=f"**>nowplaying** or **>np**", value=f"Returns your current songs info.", inline=False)
        embed.add_field(name=f"**>nowplayingalbum** or **>npa**", value=f"Returns your current songs info, track scrobbles are replaced by album scrobbles.", inline=False)
        embed.add_field(name=f"**>profile** or **>pf**", value=f"Returns a link to the Last.fm profile.", inline=False)
        embed.add_field(name=f"**>set** and **>unset**", value=f"Sets and unsets your username.", inline=False)
        embed.add_field(name=f"**>topartists** or **>ta**", value=f"Returns the top artists of the specified timeframe.", inline=False)
        embed.add_field(name=f"**>toptags** or **>tt**", value=f"Returns the top tags of the specified timeframe.", inline=False)
        embed.add_field(name=f"**>whoknows** or **>wk**", value=f"Returns the users who have listened to the artist.", inline=False)

        await ctx.author.send(embed=embed)

def setup(bot):
    bot.add_cog(help(bot))