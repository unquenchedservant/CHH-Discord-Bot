#!/usr/bin/env python3
## possible that's only needed for linux.
import discord
from discord.ext import commands
from discord.utils import get
from utilities import get_env, database

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix="^", description="A quick bot with random stuff for the CHH discord", case_insensitive=True, intents=intents)



extensions=['cogs.admin', 'cogs.reports', 'cogs.aprilfools', 'cogs.events']

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.event
async def on_member_join(member):
    if database.getRoleMemoryState(member.guild.id):
        rolesToAdd = database.getRoles(member.id)
        for roleID in rolesToAdd:
            role = get(member.guild.roles, id=roleID)
            await member.add_roles(role, atomic=True)
    database.removeRoles(member.id)
    
@bot.event
async def on_member_remove(member):
    if database.getRoleMemoryState(member.guild.id):
        for role in member.roles:
            if not role.name == "@everyone":
                database.addRole(member.id, role.id)

if __name__ == '__main__':
    for extension in extensions:
        bot.load_extension(extension)

token = get_env.discord_token()
bot.run(token, bot=True, reconnect=True)
