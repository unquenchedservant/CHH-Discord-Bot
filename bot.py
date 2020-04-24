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

def check_is_mod(user):
    is_mod = False
    for r in user.roles:
        for p in r.permissions:
            if p[0] == "administrator" and p[1] == True:
                is_mod = True
    return is_mod

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

@bot.command(hidden=True, usage="<number of messages to purge>", description="Clear the previous X messages on this channel")
@has_permissions(administrator=True)
async def clear(ctx, amount: int):
    msgs = []
    await ctx.channel.purge(limit=amount+1)

@bot.command(hidden=True, aliases=["set_prefix"], usage="<wanted_prefix>", description="Set a max 2-character prefix for this bot on this server")
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

@bot.command(hidden=True, aliases=["add"], usage="<suggestion|recommendations>", brief="Add a tracked channel", description="Start tracking a channel for suggestions or recommendations")
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

@bot.command(hidden=True, usage="<suggestions|recommendations>", brief="Remove a tracked channel", description="Remove a channel from being tracked for suggestions/recommendations")
@has_permissions(administrator=True)
async def remove(ctx, track_type=""):
    if track_type == "suggestions":
        success = database.remove_suggestion_channel(ctx.channel.id)
        if success:
            temp_message = await ctx.channel.send("No longer tracking this channel for suggestions")
        else:
            temp_message = await ctx.channel.send("Was not tracking this channel for suggestions")
        await asyncio.sleep(3)
        await ctx.message.delete()
        await temp_message.delete()
    elif track_type == "recommendations":
        success = database.remove_recommendation_channel(ctx.channel.id)
        if success:
            temp_message = await ctx.channel.send("No longer tracking this channel for recommendations")
        else:
            temp_message = await ctx.channel.send("Was not tracking this channel for recommendations")
        await asyncio.sleep(3)
        await ctx.message.delete()
        await temp_message.delete()
    else:
        embed = discord.Embed(title="Error Removing Tracking", description="Please specify one of the following", colour=0x0099ff)
        embed.set_author(name="r/CHH Bot", icon_url="https://i.imgur.com/ZNdCFKg.png")
        embed.add_field(name="suggestions", value="removes tracking for a suggestion channel")
        embed.add_field(name="\u200b", value="\u200B")
        embed.add_field(name="\u200b", value="\u200B")
        embed.add_field(name="recommendations", value="removes tracking for a recommendation channel")
        await ctx.channel.send(embed=embed)

"""Recommend an artist

Keyword arguments:
<artist name> -- the artist name you are searching
"""
@bot.command(usage="<artist name>", brief="Recommend music!", description="Recommend an artist to the given channel")
async def recommend(ctx, *args):
    allowed_channels = database.get_recommended_channels()
    search_term = ' '.join(args)
    if ctx.channel.id in allowed_channels:
        if search_term == "":
            embed = discord.Embed(title="Error Finding Artist", description="Please enter an artist name to search", colour=0x0099ff)
            embed.set_author(name="r/CHH Bot", icon_url="https://i.imgur.com/ZNdCFKg.png")
            embed.add_field(name="Usage", value="{}recommend <artist name>".format(database.get_prefix(ctx.guild.id)))
        else:
            SPOTIPY_ID = os.getenv('SPOTIPY_ID')
            SPOTIPY_SECRET = os.getenv('SPOTIPY_SECRET')
            sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=SPOTIPY_ID, client_secret=SPOTIPY_SECRET))
            results = sp.search(q=search_term, limit=10, type='artist')
            best_choice = None
            for item in results['artists']['items']:
                if item['name'].upper() == search_term.upper():
                    best_choice = item
                    break
            if not best_choice:
                items=results['artists']['items']
                if len(items) > 0:
                    artist = items[0]
            else:
                artist = best_choice
            artist_name = artist['name']
            artist_url = artist['external_urls']['spotify']
            artist_image = artist['images'][0]['url']
            artist_uri = artist['uri']
            top_tracks = sp.artist_top_tracks(artist_uri)
            top_line = ""
            for track in top_tracks['tracks'][:5]:
                top_line = top_line + track['name'] + "\n"
            related_artist = sp.artist_related_artists(artist_uri)
            related_line = ""
            for artist in related_artist['artists'][:5]:
                related_line = related_line + artist['name'] + "\n"
            embed = discord.Embed(title=artist_name, description="result for spotify search of {}".format(search_term), url=artist_url)
            embed.set_thumbnail(url=artist_image)
            embed.add_field(name="Top Tracks", value=top_line)
            embed.add_field(name="\u200b", value="\u200B")
            embed.add_field(name="Related Artists", value=related_line)
            await ctx.channel.send(embed=embed)
            await ctx.channel.send(artist_url)


token = os.getenv('DISCORD_TOKEN')
bot.run(token)
