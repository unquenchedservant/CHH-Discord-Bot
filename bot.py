#!/usr/bin/python3
import discord, logging
from discord.ext import commands
from utilities import database, get_env
from discord.utils import get
from dotenv import load_dotenv
from utilities import database

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="chh_bot.log", encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

default_prefix = "^"
async def determine_prefix(bot, message):
    guild = message.guild
    if guild:
        return database.get_prefix(guild.id)
    else:
        return default_prefix

description = '''This bot monitors the suggestion channel and also adds some process_commands that are specific to the r/chh discord server'''
bot = commands.Bot(command_prefix=determine_prefix, description=description)

if __name__ == '__main__':
    for extension in extensions:
        bot.load_extension(extension)


@bot.event
async def on_raw_reaction_add(payload):
    yes = "💯"
    no = "❌"
    user = get(bot.get_all_members(), id=payload.user_id)
    if not payload.user_id == bot.user.id:
        channel = get(bot.get_all_channels(), id=payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        if payload.channel_id in database.get_suggestion_channels() and check_is_mod(user):
            if payload.emoji.name == no:
                await message.clear_reactions()
                await message.add_reaction(no)
                await channel.send("Sorry {}, your suggestion has been denied. {} will tell you why.".format(message.author.mention, user.mention))
            elif payload.emoji.name == yes:
                await message.clear_reactions()
                await message.add_reaction(yes)
                await channel.send("Good news, {}, your suggestion has been accepted".format(message.author.mention))



@bot.event
async def on_ready():
    print('logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('----')

@bot.event
async def on_message(message):
    yes = "\U00002705"
    no = "\U0001F6AB"
    suggestion_prefixes = ["[SUBREDDIT]","[DISCORD]","[CHH_BOT]","[CHH]"]
    is_mod = check_is_mod(message.author)
    was_suggestion = False
    if message.channel.id in database.get_suggestion_channels() and not message.content.startswith(database.get_prefix(message.guild.id)):
        valid_msg = False
        content = message.content
        content = content.upper()
        for pfx in suggestion_prefixes:
            if content.startswith(pfx):
                await message.add_reaction(yes)
                await message.add_reaction(no)
                valid_msg = True
            if not valid_msg and not is_mod:
                temp_message = await message.channel.send("%s please use [SUBREDDIT], [DISCORD], [CHH_BOT] or [CHH] before your suggestion" % message.author.mention)
                await asyncio.sleep(8)
                await message.delete()
                await temp_message.delete()

    else:
        await bot.process_commands(message)
        else:

token = get_env.discord_token()
bot.run(token, bot=True, reconnect=True)
