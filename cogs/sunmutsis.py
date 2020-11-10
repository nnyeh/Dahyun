from discord.ext import commands

class sm(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def sm(self, ctx, arg=None):

        sunmutsisxd = ["yuiko", "lab", "uxen", "eng", "vroll", "lambda", "nobbi", "fejes", "kyo", None]
        sunmutsis = ""
        if arg == "yuiko":
            sunmutsis = "tvoja mama"
        elif arg == "lab":
            sunmutsis = "din mamma"
        elif arg == "uxen":
            sunmutsis = "mora di"
        elif arg == "aengus":
            sunmutsis = "twoja stara"
        elif arg == "eng":
            sunmutsis = "your mom"
        elif arg == "vroll":
            sunmutsis = "мама ти"
        elif arg == "lambda":
            sunmutsis = "你媽媽"
        elif arg == "nobbi":
            sunmutsis = "deine mutter"
        elif arg == "fejes":
            sunmutsis = "anyád"
        elif arg == "kyo":
            sunmutsis = "sua mãe"
        elif arg is None:
            sunmutsis = "sun mutsis"
        elif arg is not sunmutsisxd:
            sunmutsis = "sun mutsis"

        await ctx.message.delete()
        await ctx.send(f"{sunmutsis}")

def setup(bot):
    bot.add_cog(sm(bot))