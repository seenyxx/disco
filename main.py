from nextcord.ext import commands
from util import load_config
import cogs

config = load_config()

bot = commands.Bot(command_prefix=config['prefix'])

@bot.event
async def on_ready():
    print('Ready!')
    cogs.misc.setup(bot)

try:
    bot.run(config['token'])
except Exception as e:
    print(f'Error: failed to start the bot\n{e}')
    exit(1)                     