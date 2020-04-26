#!/usr/bin/python3
import os, discord, asyncio, sqlite3, logging, spotipy
from discord.ext import commands
from utilities import database, get_env
from discord.utils import get
from dotenv import load_dotenv
from utilities import database
from spotipy.oauth2 import SpotifyClientCredentials

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

if __name__ == '__main__':
    for extension in extensions:
        bot.load_extension(extension)

async def on_reaction_add(reaction, user):
    if not user.id == bot.user.id:
        message_id = reaction.message.id
        check_ids = database.get_reaction_message_id()
        if message_id in check_ids and (reaction.emoji == "⏭" or reaction.emoji == "⏮"):
            data = database.get_reaction_message(message_id)
            primary_id = data[0]
            second_id = data[1]
            user_id = data[2]
            page = data[3]
            if reaction.emoji == "⏭":
                page += 1
            elif reaction.emoji == "⏮":
                page -= 1
            search_string = data[4]
            if not user.id == user_id:
                await reaction.message.clear_reactions()
                if not page == 1:
                    await reaction.message.add_reaction("⏮")
                if not page == 10:
                    await reaction.message.add_reaction("⏭")
            else:
                SPOTIPY_ID = os.getenv('SPOTIPY_ID')
                SPOTIPY_SECRET = os.getenv('SPOTIPY_SECRET')
                sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=SPOTIPY_ID, client_secret=SPOTIPY_SECRET))
                results = sp.search(q=search_string, limit=10, type='artist')
                items=results['artists']['items']
                if len(items) > 0:
                    artist = items[page - 1]
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
                    embed = discord.Embed(title=artist_name, description="result for spotify search of {}".format(search_string), url=artist_url)
                    embed.set_thumbnail(url=artist_image)
                    embed.add_field(name="Top Tracks", value=top_line)
                    embed.add_field(name="\u200b", value="\u200B")
                    embed.add_field(name="Related Artists", value=related_line)
                    second_message = await reaction.message.channel.fetch_message(second_id)
                    await second_message.edit(embed=embed)
                    await reaction.message.edit(content=artist_url)
                    await reaction.message.clear_reactions()
                    if not page == 1:
                        await reaction.message.add_reaction("⏮")
                    if not page == 10:
                        await reaction.message.add_reaction("⏭")
                    database.update_reaction_page(reaction.message.id, page)
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
        else:

token = get_env.discord_token()
bot.run(token, bot=True, reconnect=True)

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
            items=results['artists']['items']
            if len(items) > 0:
                artist = items[0]
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
                second_msg = await ctx.channel.send(embed=embed)
                primary_msg = await ctx.channel.send(artist_url)
                await primary_msg.add_reaction("\U000023ED")
                database.add_reaction_message(primary_msg.id, second_msg.id, ctx.message.author.id, search_term)