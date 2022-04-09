#!/usr/bin/python3
from discord.ext import commands
from discord.utils import get
from utilities import get_env

bot = commands.Bot(command_prefix="^", description="A quick bot with random stuff for the CHH discord", case_insensitive=True)



extensions=['cogs.admin', 'cogs.reports', 'cogs.aprilfools']

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

if __name__ == '__main__':
    for extension in extensions:
        bot.load_extension(extension)

token = get_env.discord_dev()
bot.run(token, bot=True, reconnect=True)
