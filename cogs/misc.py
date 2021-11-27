from nextcord.ext import commands
from math import floor

class Misc(commands.Cog):
    """ Misc commands """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping')
    async def ping(self, ctx):
        await ctx.reply(f'Pong! {floor(self.bot.latency * 1000)}ms')

def setup(bot):
    """Setup miscellaneous commands """
    bot.add_cog(Misc(bot))