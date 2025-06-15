#!/usr/bin/env python3
## possible that's only needed for linux.
import sys

import discord
import utilities
from discord.ext import commands
from discord.utils import get
from utilities import get_env
from utilities.database import StarboardSettings, RoleMemory, Role, Birthday
from utilities.logging import logger
from utilities import logging
import sqlite3
import asyncio

intents = discord.Intents.all()
intents.members = True
intents.reactions = True
intents.messages = True

starboard_settings = StarboardSettings()
role_memory = RoleMemory()
role = Role()
birthday = Birthday()

bot = discord.Bot(
    debug_guilds=[utilities.DEV_GUILD_ID], owner_id=utilities.OWNER_ID, intents=intents
)

extensions = [
    "cogs.admin",
    "cogs.aprilfools",
    "cogs.birthdays",
    "cogs.events",
    "cogs.selfpromo",
    "cogs.starboard"
]

@bot.event
async def on_ready():
    logger.info("We have logged in as {0.user}".format(bot))
    conn = sqlite3.connect("chh.db")
    if not starboard_settings.check(utilities.GUILD_ID):
        starboard_settings.add(utilities.GUILD_ID, utilities.STARBOARD_CHANNEL_ID, 5)

@bot.event
async def on_member_join(member):
    if role_memory.get(member.guild.id):
        rolesToAdd = role.get(member.id)
        birthday.set_active(True, member.id)
        for roleID in rolesToAdd:
            role = get(member.guild.roles, id=roleID)
            await member.add_roles(role, atomic=True)
    role.remove(member.id)

@bot.event
async def on_member_remove(member):
    birthday.set_active(False, member.id)
    if role_memory.get(member.guild.id):
        for role in member.roles:
            if not role.name == "@everyone":
                role.add(member.id, role.id)

async def sync_commands():
    await bot.sync_commands()

if __name__ == "__main__":
    if "--dev" in sys.argv:
        logging.setLoggerLevel(True)
        utilities.set_is_dev(True)
        logger.info("Running Developer Bot")
        for extension in extensions:
            bot.load_extension(extension)
        token = get_env.discord_dev()
        bot.run(token)
    else:
        utilities.set_is_dev(False)
        logging.setLoggerLevel(False)
        for extension in extensions:
            bot.load_extension(extension)
        token = get_env.discord_token()
        bot.run(token)
