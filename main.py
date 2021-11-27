from nextcord.ext import commands
from nextcord.embeds import Embed
from util import load_config
import cogs
from util.logs import log_msg

config = load_config()

bot = commands.Bot(command_prefix=config['prefix'])
bot.remove_command('help')

@bot.event
async def on_ready():
    print('Ready!')
    cogs.misc.setup(bot)

try:
    bot.run(config['token'])
except Exception as e:
    print(f'Error: failed to start the bot\n{e}')
    exit(1)                     

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = Embed(title='You cannot use this command yet! ⌚',description='Try again in **{:.2f} seconds**'.format(error.retry_after), color=0x001b3b)
        await ctx.send(embed=embed)
    else:
        print(error)
        log_msg(error)