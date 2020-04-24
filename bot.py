#!/usr/bin/python3
import os, discord, asyncio, sqlite3, logging
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv
from utilities import database
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="chh_bot.log", encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

@bot.event
async def on_message(message):
    if message.author.id = self.user.id:
        return
    await bot.process_commands(message)





client = chh_bot()
TOKEN=os.getenv('DISCORD_TOKEN')
client.run(TOKEN)
