from nextcord.ext import commands
from nextcord.embeds import Embed
from math import floor
from copy import deepcopy
from nextcord.ext.commands.context import Context
from util import error_too_many_args
from util.messages import error_help_menu_notfound

help_menu_color = 0x52b7ff

class Misc(commands.Cog):
    """ Misc commands """
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name='ping')
    async def ping(self, ctx: Context):
        """ Ping command """

        await ctx.reply(f'Pong! {floor(self.bot.latency * 1000)}ms')

    @commands.command(name='help')
    async def help(self, ctx: Context, *cog):
        """ Shows this menu """

        if not cog:
            embed = Embed(title='Help', color=help_menu_color)

            cogs_text = ''
            for c in self.bot.cogs:
                cogs_text += f'**{c}** - {self.bot.cogs[c].__doc__}'

            embed.add_field(name='Categories', value=cogs_text[0: len(cogs_text) - 1])

            await ctx.send(embed=embed)
        else:
            found = False
            if len(cog) > 1:
                await ctx.send(embed=error_too_many_args())
            else:
                for c in self.bot.cogs:
                    for ac in cog:
                        if c.lower() == ac.lower():
                            embed = Embed(title=f'Help for {cog[0]}', color=help_menu_color)
                            commands_text = ''
                            for cmd in self.bot.get_cog(ac.title()).get_commands():
                                if not cmd.hidden:
                                    commands_text += f'[{cmd.name}] - {cmd.help}\n'
                            
                            embed.add_field(name='Commands', value=f'```ini\n{commands_text}```')
                            await ctx.send(embed=embed)
                            found = True
                
                if not found:
                    for c in self.bot.cogs: 
                        for cmd in self.bot.get_cog(c).get_commands():
                            if cmd.name.lower() == cog[0].lower():
                                embed = Embed(title=f'{cmd.name.lower()}', description=f'**Info:** {cmd.qualified_name} \n**Usage:** ```fix\n{cmd.qualified_name} {cmd.signature}```', color=help_menu_color)
                                await ctx.send(embed=embed)
                                found = True

                    if not found:
                        await ctx.send(embed=error_help_menu_notfound())





def setup(bot):
    """Setup miscellaneous commands """
    bot.add_cog(Misc(bot))