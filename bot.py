#!/usr/bin/env python3
## possible that's only needed for linux.
import sys

import discord
import utilities
from utilities import Config
from discord.ext import commands
from discord.utils import get
from utilities import get_env
from utilities.database import StarboardSettings, RoleMemory, Role, Birthday
from utilities.logging import logger
from utilities import logging

config = Config()
intents = discord.Intents.all()
intents.members = True
intents.reactions = True
intents.messages = True

starboard_settings = StarboardSettings()
role_memory = RoleMemory()
role_db = Role()
birthday = Birthday()

bot = discord.Bot(
    debug_guilds=[config.CHH_GUILD_ID], owner_id=config.OWNER_ID, intents=intents
)

extensions = [
    "cogs.admin",
    "cogs.birthdays",
    "cogs.events",
    "cogs.selfpromo",
    "cogs.starboard"
]

@bot.event
async def on_ready():
    logger.info("We have logged in as {0.user}".format(bot))
    if not starboard_settings.check(config.get_guild_id()):
        starboard_settings.add(config.get_guild_id(), config.get_starboard_channel(), 5)

@bot.event
async def on_member_join(member):
    if role_memory.get(member.guild.id):
        rolesToAdd = role.get(member.id)
        birthday.set_active(True, member.id)
        for roleID in rolesToAdd:
            role = get(member.guild.roles, id=roleID)
            await member.add_roles(role, atomic=True)
        role_db.remove(member.id)

@bot.event
async def on_member_remove(member):
    birthday.set_active(False, member.id)
    if role_memory.get(member.guild.id):
        for role in member.roles:
            if not role.name == "@everyone":
                role_db.add(member.id, role.id)

if __name__ == "__main__":
    if "--dev" in sys.argv:
        logging.setLoggerLevel(True)
        config.is_dev = True
        logger.info("Running Developer Bot")
        for extension in extensions:
            bot.load_extension(extension)
        token = get_env.discord_dev()
        bot.run(token)
    else:
        config.is_dev = False
        logging.setLoggerLevel(False)
        for extension in extensions:
            bot.load_extension(extension)
        token = get_env.discord_token()
        bot.run(token)
