#!/usr/bin/python3
import os, discord, asyncio, sqlite3, logging, spotipy
from discord.ext import commands
from discord.ext.commands import has_permissions, CheckFailure
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
@has_permissions(administrator=True)
async def clear(ctx, amount: int):
    msgs = []
    await ctx.channel.purge(limit=amount+1)

@bot.command()
@has_permissions(administrator=True)
async def prefix(ctx, new_prefix=""):
    if new_prefix == "":
        embed = discord.Embed(title="Prefix", description="Get or change the server prefix", colour=0x0099ff)
        embed.set_author(name="r/CHH Bot", icon_url="https://i.imgur.com/ZNdCFKg.png")
        embed.add_field(name="Current prefix", value="{}".format(database.get_prefix(ctx.guild.id)))
        embed.add_field(name="\u200B", value="\u200B")
        embed.add_field(name="\u200B", value="\u200B")
        embed.add_field(name="Change Prefix", value="To change the prefix, use {}prefix <new prefix>".format(database.get_prefix(ctx.guild.id)), inline=True)
        await ctx.channel.send(embed=embed)
    else:
        if len(new_prefix) > 2:
            embed = discord.Embed(title="Invalid Prefix", description="Please make sure that your prefix is at max two characters", colour=0x0099ff)
            embed.set_author(name="r/CHH Bot", icon_url="https://i.imgur.com/ZNdCFKg.png")
            embed.add_field(name="Change Prefix", value="To change the prefix, use {}prefix <new prefix>".format(database.get_prefix(ctx.guild.id)), inline=True)
            await ctx.channel.send(embed=embed)
        else:
            database.set_prefix(ctx.guild.id, new_prefix)
            await ctx.channel.send("Successfully updated prefix for server")

@bot.command()
@has_permissions(administrator=True)
async def track(ctx, track_type=""):
    if track_type == "suggestions":
        success = database.add_suggestion_channel(ctx.channel.id)
        if success:
            temp_message = await ctx.channel.send("Now tracking this channel for suggestions")
        else:
            temp_message = await ctx.channel.send("Already tracking this channel for suggestions")
        await asyncio.sleep(3)
        await ctx.message.delete()
        await temp_message.delete()
    elif track_type == "recommendations":
        success = database.add_recommendation_channel(ctx.channel.id)
        if success:
            temp_message = await ctx.channel.send("Now tracking this channel for recommendations")
        else:
            temp_message = await ctx.channel.send("Already tracking this channel for suggestions")
        await asyncio.sleep(3)
        await ctx.message.delete()
        await temp_message.delete()
    else:
        embed = discord.Embed(title="Error Adding Tracking", description="Please specify one of the following", colour=0x0099ff)
        embed.set_author(name="r/CHH Bot", icon_url="https://i.imgur.com/ZNdCFKg.png")
        embed.add_field(name="suggestions", value="tracks a suggestion channel")
        embed.add_field(name="\u200b", value="\u200B")
        embed.add_field(name="\u200b", value="\u200B")
        embed.add_field(name="recommendations", value="tracks a recommendation channel")
        await ctx.channel.send(embed=embed)
token = os.getenv('DISCORD_TOKEN')
bot.run(token)
