#!/usr/bin/python3
import os, discord, asyncio, sqlite3, logging, spotipy
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv
from utilities import database
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()
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

@bot.event
async def on_ready():
    print('logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('----')

@bot.event
async def on_message(message):

    await bot.process_commands(message)

@bot.command()
async def clear(ctx, amount: int):
    msgs = []
    await ctx.channel.purge(limit=amount+1)




token = os.getenv('DISCORD_TOKEN')
bot.run(token)
