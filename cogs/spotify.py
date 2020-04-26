#!/usr/bin/python3
import discord, spotipy
from discord.ext import commands
from discord.utils import get
from utilities import database, get_env
from spotipy.oauth2 import SpotifyClientCredentials

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.spotify= spotipy.Spotify(client_credentials_manager=get_env.spotify_credentials())

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
                    results = self.spotify.search(q=search_string, limit=10, type='artist')
                    items=results['artists']['items']
                    if len(items) > 0:
                        artist = items[page - 1]
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

    @commands.command(usage="<artist name>", brief="Recommend music!", description="Recommend an artist to the given channel")
    async def recommend(self, ctx, *args):
        allowed_channels = database.get_recommended_channels()
        search_term = ' '.join(args)
        if ctx.channel.id in allowed_channels:
            if search_term == "":
                embed = discord.Embed(title="Error Finding Artist", description="Please enter an artist name to search", colour=0x0099ff)
                embed.set_author(name="r/CHH Bot", icon_url="https://i.imgur.com/ZNdCFKg.png")
                embed.add_field(name="Usage", value="{}recommend <artist name>".format(database.get_prefix(ctx.guild.id)))
            else:
                results = self.spotify.search(q=search_term, limit=10, type='artist')
                items=results['artists']['items']
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
                    await primary_msg.add_reaction("\U000023ED")
                    database.add_reaction_message(primary_msg.id, second_msg.id, ctx.message.author.id, search_term)

def setup(bot):
    bot.add_cog(Music(bot))
