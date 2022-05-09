#!/usr/bin/env python3
## possible that's only needed for linux.
import discord
from discord.ext import commands
from discord.utils import get
from utilities import get_env, database

intents = discord.Intents.all()
intents.members = True

bot = discord.Bot(debug_guilds=[365879579887534080], owner_id=236394260553924608,intents=intents)



extensions=['cogs.admin']

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

#token = get_env.discord_token()
token = get_env.discord_dev()
bot.run(token)
