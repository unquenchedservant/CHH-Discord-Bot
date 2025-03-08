#!/usr/bin/env python3
## possible that's only needed for linux.
import sys

import discord
import utilities
from discord.ext import commands
from discord.utils import get
from utilities import database, get_env
from utilities.logging import logger
from utilities import logging
import sqlite3
import asyncio

intents = discord.Intents.all()
intents.members = True
intents.reactions = True
intents.messages = True

bot = discord.Bot(
    debug_guilds=[365879579887534080], owner_id=236394260553924608, intents=intents
)

extensions = [
    "cogs.admin",
    "cogs.aprilfools",
    "cogs.birthdays",
    "cogs.events",
    "cogs.selfpromo",
    "cogs.starboard",
]

@bot.event
async def on_ready():
    logger.info("We have logged in as {0.user}".format(bot))
    conn = sqlite3.connect("chh.db")
    if not database.checkStarboardSettings(utilities.get_guild_id()):
        database.addStarboardSettings(utilities.get_guild_id(), utilities.get_starboard_channel(), 5)

@bot.event
async def on_member_join(member):
    if database.getRoleMemoryState(member.guild.id):
        rolesToAdd = database.getRoles(member.id)
        database.setBirthdayActive(True, member.id)
        for roleID in rolesToAdd:
            role = get(member.guild.roles, id=roleID)
            await member.add_roles(role, atomic=True)
    database.removeRoles(member.id)

@bot.event
async def on_member_remove(member):
    database.setBirthdayActive(False, member.id)
    if database.getRoleMemoryState(member.guild.id):
        for role in member.roles:
            if not role.name == "@everyone":
                database.addRole(member.id, role.id)

async def sync_commands():
    await bot.sync_commands()

if __name__ == "__main__":
    tasks = set()
    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    if "--dev" in sys.argv:
        logging.setLoggerLevel(True)
        utilities.set_is_dev(True)
        logger.info("Running Developer Bot")
        for extension in extensions:
            bot.load_extension(extension)
        task = loop.create_task(sync_commands())
        tasks.add(task)
        task.add_done_callback(tasks.discard)
        token = get_env.discord_dev()
        bot.run(token)
    else:
        utilities.set_is_dev(False)
        logging.setLoggerLevel(False)
        for extension in extensions:
            bot.load_extension(extension)
        task = loop.create_task(sync_commands())
        tasks.add(task)
        task.add_done_callback(tasks.discard)
        token = get_env.discord_token()
        bot.run(token)
