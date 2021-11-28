from nextcord.ext import commands
from nextcord.embeds import Embed
from util import load_config
import cogs
from util.logs import log_msg
from util.messages import error_embed

config = load_config()

bot = commands.Bot(command_prefix=config['prefix'])
bot.remove_command('help')

@bot.event
async def on_ready():
    print('Ready!')
    cogs.misc.setup(bot)
    cogs.voice.setup(bot)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = Embed(title='You cannot use this command yet! ⌚',description='Try again in **{:.2f} seconds**'.format(error.retry_after), color=0x001b3b)
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send(embed=error_embed(f'**Missing Permissions**\n{error}'))
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send(embed=error_embed(f'**I am missing permissions**\n{error}'))
    else:
        log_msg(error)
        print(error)

try:
    bot.run(config['token'])
except Exception as e:
    log_msg(f'Error: failed to start the bot\n{e}')
    print(f'Error: failed to start the bot\n{e}')
    exit(1)                     