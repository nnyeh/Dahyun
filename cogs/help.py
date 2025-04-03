import discord
from discord.ext import commands

class help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        try:
            embed = discord.Embed(
                title="Commands",
                description=(
                    "With some commands you can specify the member of whose data you want to return with a mention. "
                    "You can also specify the artist and/or album with **[artist] | [album]** with some commands but if you do not specify them "
                    "and you have your Last.fm username set on the server, it will return the data of whatever you're currently listening to.\n\n"
                    "Some commands can be specified to use a different time frame:\n"
                    "**w: week**\n**m: month**\n**q: quarter**\n**s: semester**\n**y: year**\n**a: alltime**\n"
                    "If no timeframe is specified, it defaults to a week."
                ),
                colour=0x4a5fc3
            )

            embed.add_field(name="**>albumcover** or **>co**", value="Returns the album cover from Last.fm.", inline=False)
            embed.add_field(name="**>albumcoverspotify** or **>sco**", value="Returns the album cover from Spotify.", inline=False)
            embed.add_field(name="**>albuminfo** or **>abi**", value="Returns the album info.", inline=False)
            embed.add_field(name="**>artistinfo** or **>ai**", value="Returns the artist info.", inline=False)
            embed.add_field(name="**>combo**", value="Displays the amount of plays of the same artist, album or song.", inline=False)
            embed.add_field(name="**>genreinfo** or **>gi**", value="Returns info about a specified genre.", inline=False)
            embed.add_field(name="**>spotify** or **>sp**", value="Returns a Spotify link.", inline=False)
            embed.add_field(name="**>youtube** or **>yt**", value="Returns a YouTube link.", inline=False)
            embed.add_field(name="**>github** or **>git**", value="Returns the Github link.", inline=False)
            embed.add_field(name="**>lyrics**", value="Returns the lyrics from Genius.com.", inline=False)
            embed.add_field(name="**>nowplaying** or **>np**", value='Returns your current song\'s info. Add "a" or "album" after the command to switch track plays to album plays.', inline=False)
            embed.add_field(name="**>profile** or **>pf**", value="Returns a link to the Last.fm profile.", inline=False)
            embed.add_field(name="**>set** and **>unset**", value="Sets and unsets your username.", inline=False)
            embed.add_field(name="**>topartists** or **>ta**", value="Returns the top artists of the specified timeframe.", inline=False)
            embed.add_field(name="**>toptags** or **>tt**", value="Returns the top tags of the specified timeframe.", inline=False)
            embed.add_field(name="**>whoknows** or **>wk**", value="Returns the users who have listened to the artist.", inline=False)

            try:
                await ctx.send("`Sent you a direct message.`")
                await ctx.author.send(embed=embed)
            except discord.Forbidden:
                await ctx.send("`Enable direct messages for this server to use this command.`")

        except Exception as e:
            print(f"Error in help command: {e}")
            await ctx.send("An error occurred while processing the help command.")

async def setup(bot):
    await bot.add_cog(help(bot))