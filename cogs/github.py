from discord.ext import commands

class github(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["git"])
    async def github(self, ctx):

        await ctx.send(f"https://github.com/nnyeh/dahyun")

def setup(bot):
    bot.add_cog(github(bot))