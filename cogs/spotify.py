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

    async def get_tracks(self, song_list, info_type, no_line):
        line = ""
        if not len(song_list[info_type]) == 0:
            if len(song_list[info_type]) < 5:
                amount = len(song_list)
            else:
                amount = 5
            for track in song_list[info_type][:amount]:
                line = line + track['name'] + "\n"
        if line == "":
            line = "No {}".format(no_line)
        return line

    async def get_spotify(self, search, items, cur_page, user, search_type, owner=None):
        best_match_index = -1
        potential_match = -1
        found_exact = False
        x = 0
        for term in items:
            if search_type == "playlist" and not owner == None:
                if term['name'] == search:
                    if owner == term['owner']['display_name']:
                        best_match_index = x
                        found_exact = True
                    else:
                        potential_match = x
            else:
                if term['name'].lower() == search.lower():
                    best_match_index = x
                    found_exact = True
            x += 1
        if found_exact == False:
            best_match_index = potential_match
        if best_match_index > -1:
            temp_store = items[0]
            items[0] = items[best_match_index]
            items[best_match_index] = temp_store
        item         = items[cur_page - 1]
        max_page     = len(items)
        title        = item['name']
        url          = item['external_urls']['spotify']

        if not (search_type == "artist" or search_type == "playlist"):
            artist = item['artists'][0]['name']
            title  = "{} - {}".format(title, artist)

        if search_type == "artist":
            h1    = "Top Tracks"
            info1 = await self.get_tracks(self.spotify.artist_top_tracks(item['uri']), 'tracks', h1)
            h2    = "Related Artists"
            info2 = await self.get_tracks(self.spotify.artist_related_artists(item['uri']), 'artists', h2)

        if search_type == "album":
            h1    = "Release Date"
            info1 = item["release_date"]
            h2    = "Tracks"
            info2 = item["total_tracks"]

        if search_type == "track":
            h1    = "Album"
            info1 = item['album']['name']
            h2    = "Release Year"
            info2 = item['album']['release_date'].split("-")[0]

        if search_type == "playlist":
            h1    = "Creator"
            info1 = item['owner']['display_name']
            h2    = "Tracks"
            info2 = item['tracks']['total']

        embed        = await self.get_embed(title, search_type, url, h1, h2, info1, info2, user, cur_page, max_page)

        return [embed, url]

    async def get_embed(self, title, search_type, url, h1, h2, info1, info2, user, cur_page, max_page):
        embed = discord.Embed(title=title, url=url)
        embed.set_author(name="Search ran by {}.".format(user.name), icon_url=user.avatar_url)
        embed.add_field(name=h1, value=info1)
        embed.add_field(name="\u200b", value="\u200B")
        embed.add_field(name=h2, value=info2)
        embed.set_footer(text="{}s | Page {} of {}".format(search_type, cur_page, max_page))
        return embed

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if not user.id == self.bot.user.id:
            message_id = reaction.message.id
            check_ids = database.get_reaction_message_id()
            if message_id in check_ids and (reaction.emoji == "⏭" or reaction.emoji == "⏮"):
                prim_id, sec_id, uid, page, search, search_type = database.get_reaction_message(message_id)

                if reaction.emoji == "⏭":
                    page += 1
                elif reaction.emoji == "⏮":
                    page -= 1
                if not user.id == uid:
                    await reaction.message.clear_reactions()
                    if not page == 1:
                        await reaction.message.add_reaction("⏮")
                    if not page == 50:
                        await reaction.message.add_reaction("⏭")
                else:
                    if search_type == "playlist":
                        if " && " in search:
                            temp = search.split(" && ")
                            search = temp[0]
                            owner = temp[1]
                        else:
                            owner = None
                    results = self.spotify.search(q=search, limit=50, type=search_type)
                    items   = results["{}s".format(search_type)]['items']
                    second_message = await reaction.message.channel.fetch_message(sec_id)
                    if len(items) > 0:
                        if search_type == "artist":
                            embed, url = await self.get_spotify(search, items, page, user, 'artist')

                        elif search_type == "album":
                            embed, url = await self.get_spotify(search, items, page, user, 'album')

                        elif search_type == "track":
                            embed, url = await self.get_spotify(search, items, page, user, 'track')

                        elif search_type == "playlist":
                            embed, url = await self.get_spotify(search, items, page, user, 'playlist', owner)
                        await second_message.edit(embed=embed)
                        await reaction.message.edit(content=url)

                        await reaction.message.clear_reactions()

                        if not page == 1:
                            await reaction.message.add_reaction("⏮")

                        if not page == 50 and not int(page) == len(items):
                            await reaction.message.add_reaction("⏭")

                        database.update_reaction_page(reaction.message.id, page)

    @commands.command(name="artist", aliases=["art", "ar", "band"], brief="Recommend an artist", description="Get the top 10 on spotify of an artist")
    async def _artist(self, ctx, *args):
        await self.get_messages(ctx, args, 'artist')

    @commands.command(name="album", aliases=["al"], brief="Recommend an album", description="Display an album from spotify. Include the artist name for a better match")
    async def _album(self, ctx, *args):
        await self.get_messages(ctx, args, 'album')

    @commands.command(name="song", aliases=["track", "s"], brief="Recommend a song", description="Display a song from spotify. Include the artist name for a better match.")
    async def _song(self, ctx, *args):
        await self.get_messages(ctx, args, 'track')

    @commands.command(name="playlist", aliases=["playlists", "p"], brief="Recommend a playlist. Use ' && ' to include a Spotify user name", description="Display a playlist from spotify. Include ' &&  playlistcreatorusername' for a better match.")
    async def _playlist(self, ctx, *args):
        await self.get_messages(ctx, args, 'playlist')

    async def get_messages(self, ctx, args, search_type):
        search = ' '.join(args)
        if ctx.channel.id in database.get_recommended_channels():
            if not search == "":
                if " && " in search:
                    temp = search.split(" && ")
                    search = temp[0]
                    owner = temp[1]
                else:
                    owner = None
                results = self.spotify.search(q=search, limit=50, type=search_type)
                items = results['{}s'.format(search_type)]['items']
                if len(items) > 0:
                    if search_type == "artist":
                        embed, url = await self.get_spotify(search, items, 1, ctx.message.author, 'artist')
                    elif search_type == "album":
                        embed, url = await self.get_spotify(search, items, 1, ctx.message.author, 'album')
                    elif search_type == "track":
                        embed, url  = await self.get_spotify(search, items, 1, ctx.message.author, 'track')
                    elif search_type == "playlist":
                        embed, url  = await self.get_spotify(search, items, 1, ctx.message.author, 'playlist', owner)
                    second_msg = await ctx.channel.send(embed=embed)
                    primary_msg = await ctx.channel.send(url)

                    await ctx.message.delete()

                    if not len(items) == 1:
                        await primary_msg.add_reaction("⏭")

                    second_id = second_msg.id
                    database.add_reaction_message(primary_msg.id, second_id, ctx.message.author.id, search, search_type)

def setup(bot):
    bot.add_cog(Music(bot))
