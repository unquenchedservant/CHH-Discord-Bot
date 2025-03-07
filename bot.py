#!/usr/bin/env python3
## possible that's only needed for linux.
import sys

import discord
import utilities
from discord.ext import commands
from discord.utils import get
from utilities import database, get_env
from utilities.logging import logger

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
]

@bot.event
async def on_ready():
    logger.info("We have logged in as {0.user}".format(bot))

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

if __name__ == "__main__":

    if "--dev" in sys.argv:
        logger.info("Running Developer Bot")
        utilities.set_is_dev(True)
        for extension in extensions:
            bot.load_extension(extension)
        token = get_env.discord_dev()
        bot.run(token)
    else:
        for extension in extensions:
            bot.load_extension(extension)
        token = get_env.discord_token()
        bot.run(token)
