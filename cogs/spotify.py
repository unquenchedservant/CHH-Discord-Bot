#!/usr/bin/python3
import discord, spotipy
from discord.ext import commands
from discord.utils import get
from discord.ext.commands import group
from utilities import database, get_env
from spotipy.oauth2 import SpotifyClientCredentials

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.spotify= spotipy.Spotify(client_credentials_manager=get_env.spotify_credentials())
        self.allowed_channels = database.get_recommended_channels()

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if not user.id == self.bot.user.id:
            message_id = reaction.message.id
            check_ids = database.get_reaction_message_id()
            if message_id in check_ids and (reaction.emoji == "⏭" or reaction.emoji == "⏮"):
                data = database.get_reaction_message(message_id)
                primary_id = data[0]
                second_id = data[1]
                user_id = data[2]
                page = data[3]
                search_type = data[5]
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
                    results = self.spotify.search(q=search_string, limit=10, type=search_type)
                    items=results["{}s".format(search_type)]['items']
                    second_message = await reaction.message.channel.fetch_message(second_id)
                    if len(items) > 0:
                        result = items[page - 1]
                        if search_type == "artist":
                            artist_name = result['name']
                            url = result['external_urls']['spotify']
                            image = result['images'][0]['url']
                            artist_uri = result['uri']
                            top_tracks = self.spotify.artist_top_tracks(artist_uri)
                            top_line = ""
                            if not len(top_tracks['tracks']) == 0:
                                if len(top_tracks['tracks']) < 5:
                                    amount = len(top_tracks)
                                else:
                                    amount = 5
                                for track in top_tracks['tracks'][:amount]:
                                    top_line = top_line + track['name'] + "\n"
                            else:
                                top_line="No Top Tracks"
                            related_artist = self.spotify.artist_related_artists(artist_uri)
                            related_line = ""
                            if not len(related_artist['artists']) == 0:
                                if len(related_artist['artists']) < 5:
                                    amount = len(related_artist['artists'])
                                else:
                                    amount = 5
                                for artist in related_artist['artists'][:amount]:
                                    related_line = related_line + artist['name'] + "\n"
                            else:
                                related_line = "No Related Artists"
                            embed = discord.Embed(title=artist_name, description="result for spotify search of {}".format(search_string), url=url)
                            embed.set_thumbnail(url=image)
                            embed.add_field(name="Top Tracks", value=top_line)
                            embed.add_field(name="\u200b", value="\u200B")
                            embed.add_field(name="Related Artists", value=related_line)
                            await second_message.edit(embed=embed)
                        elif search_type == "album":
                            album_name = result['name']
                            artist_name = result['artists'][0]['name']
                            url = result['external_urls']['spotify']
                            image = result['images'][0]['url']
                            album_id = result['id']
                            album = self.spotify.album(album_id)
                            album_label = album["label"]
                            release_date = album["release_date"]
                            embed = discord.Embed(title="{} - {}".format(album_name, artist_name), description="result for spotify search of {}".format(search_string), url=url)
                            embed.set_thumbnail(url=image)
                            embed.add_field(name="Release Date", value=release_date)
                            embed.add_field(name="\u200b", value="\u200B")
                            embed.add_field(name="\u200b", value="\u200B")
                            embed.add_field(name="Label", value=album_label)
                            await second_message.edit(embed=embed)
                        await reaction.message.edit(content=url)
                        await reaction.message.clear_reactions()
                        if not page == 1:
                            await reaction.message.add_reaction("⏮")
                        if not page == 10 and not int(page) == len(items):
                            await reaction.message.add_reaction("⏭")
                        database.update_reaction_page(reaction.message.id, page)

    @commands.group(invoke_without_command=True, pass_context=True, aliases=["rec", "music", "listento"], brief="Recommend music!", description="Recommend an artist to the given channel")
    async def recommend(self, ctx, **args):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title="Invalid Command", description="Please specify one of the following", colour=0x0099ff)
            embed.set_author(name="r/CHH Bot", icon_url="https://i.imgur.com/ZNdCFKg.png")
            embed.add_field(name="artist", value="Recommend an artist")
            embed.add_field(name="\u200b", value="\u200B")
            embed.add_field(name="\u200b", value="\u200B")
            embed.add_field(name="album", value="Recommend an album")
            await ctx.channel.send(embed=embed)


    @recommend.command(name="artist")
    async def _artist(self, ctx, *args):
        search_term = ' '.join(args)
        if ctx.channel.id in self.allowed_channels:
            if not search_term == "":
                results = self.spotify.search(q=search_term, limit=10, type='artist')
                items = results['artists']['items']
                if len(items) > 0:
                    artist = items[0]
                    artist_name = artist['name']
                    artist_url = artist['external_urls']['spotify']
                    artist_image = artist['images'][0]['url']
                    artist_uri = artist['uri']
                    top_tracks = self.spotify.artist_top_tracks(artist_uri)
                    top_line = ""
                    for track in top_tracks['tracks'][:5]:
                        top_line = top_line + track['name'] + "\n"
                    related_artist = self.spotify.artist_related_artists(artist_uri)
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
                    if not len(items) == 1:
                        await primary_msg.add_reaction("⏭")
                    database.add_reaction_message(primary_msg.id, second_msg.id, ctx.message.author.id, search_term, "artist")

    @recommend.command(pass_context=True, name="album")
    async def _album(self, ctx, *args):
        search_term = ' '.join(args)
        if ctx.channel.id in self.allowed_channels:
            if not search_term == "":
                results = self.spotify.search(q=search_term, limit=10, type='album')
                items = results['albums']['items']
                if len(items) > 0:
                    album = items[0]
                    album_name = album['name']
                    album_url = album['external_urls']['spotify']
                    album_image = album['images'][0]['url']
                    artist_name = album['artists'][0]['name']
                    album_id = album['id']
                    album_details = self.spotify.album(album_id)
                    album_label = album_details["label"]
                    release_date = album_details["release_date"]
                    embed = discord.Embed(title="{} - {}".format(album_name, artist_name), description="result for spotify search of {}".format(search_term), url=album_url)
                    embed.set_thumbnail(url=album_image)
                    embed.add_field(name="Release Date", value=release_date)
                    embed.add_field(name="\u200b", value="\u200B")
                    embed.add_field(name="\u200b", value="\u200B")
                    embed.add_field(name="Label", value=album_label)
                    second_msg = await ctx.channel.send(embed=embed)
                    primary_msg = await ctx.channel.send(album_url)
                    if not len(items) == 1:
                        await primary_msg.add_reaction("⏭")
                    database.add_reaction_message(primary_msg.id, second_msg.id, ctx.message.author.id, search_term, "album")
def setup(bot):
    bot.add_cog(Music(bot))
