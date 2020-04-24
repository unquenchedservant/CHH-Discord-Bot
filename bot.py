#!/usr/bin/python3
import os, discord, asyncio, sqlite3
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv
from utilities import database
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()

class chh_bot(discord.Client):

    async def on_ready(self):
        database.create_table()
        print("Logged on as {0}!".format(self.user))

    async def on_raw_reaction_add(self, payload):
        denied = "❌"
        accepted = "💯"
        channel_ids = database.get_allowed_channels()
        if payload.channel_id in channel_ids:
            is_mod = False
            user = get(self.get_all_members(), id=payload.user_id)
            if not user == self.user:
                channel = get(self.get_all_channels(), id=payload.channel_id)
                message = await channel.fetch_message(payload.message_id)
                for r in user.roles:
                    for p in r.permissions:
                        if p[0] == "administrator" and p[1] == True:
                            is_mod = True
                if is_mod:
                    if payload.emoji.name == denied:
                        await channel.send("Sorry {}, your suggestion has been denied. {} will tell you why.".format(message.author.mention, user.mention))
                    elif payload.emoji.name == accepted:
                        await channel.send("Good news, {}, your suggestion has been accepted".format(message.author.mention))

    async def on_message(self, message):
        yes = "\U00002705"
        no = "\U0001F6AB"


        server_id = message.guild.id
        database.add_server(server_id, "^")

        if not os.path.exists("chh.db"):
            database.create_table()
            database.add_server(server_id, "&")

        cmd_prefix = database.get_prefix(server_id)

        channel_ids = database.get_allowed_channels()
        recommended_channel_ids = database.get_allowed_recommended_channels()

        suggestion_prefixs = ["[SUBREDDIT]","[DISCORD]","[CHH]"]

        is_mod = False

        for r in message.author.roles:
            for p in r.permissions:
                if p[0] == "administrator" and p[1] == True:
                    is_mod = True

        if message.author == self.user:
            return
        # START MOD COMMANDS
        else:
            if is_mod:
                # ADD CHANNEL TO MONITORING
                if message.content.startswith("{}add".format(cmd_prefix)):
                    directive = message.content.replace("{}add".format(cmd_prefix), "")
                    directive = directive.replace(" ", "")
                    if directive  == "recommended":
                        database.add_recommended_channel(message.channel.id)
                        temp_message = await message.channel.send('Added this channel to monitored channels')
                        await message.delete()
                        await asyncio.sleep(3)
                        await temp_message.delete()
                    elif directive == "suggestion":
                        database.add_channels(message.channel.id)
                        temp_message = await message.channel.send('Added this channel to monitored channels')
                        await message.delete()
                        await asyncio.sleep(3)
                        await temp_message.delete()
                    else:
                        await message.channel.send("Unknown command, use '{0}add recommended' or '{0}add suggestion' ".format(cmd_prefix))


                # REMOVE CHANNEL FROM MONITORING
                elif message.content.startswith("{}remove".format(cmd_prefix)):
                    directive = message.content.replace("{}remove".format(cmd_prefix), "")
                    directive = directive.replace(" ", "")
                    if directive  == "recommended":
                        database.remove_recommended_channel(message.channel.id)
                        temp_message = await message.channel.send('No longer monitoring this channel')
                        await message.delete()
                        await asyncio.sleep(3)
                        await temp_message.delete()
                    elif directive == "suggestion":
                        database.remove_channel(message.channel.id)
                        temp_message = await message.channel.send('No longer monitoring this channel')
                        await message.delete()
                        await asyncio.sleep(3)
                        await temp_message.delete()
                    else:
                        await message.channel.send("Unknown command, use '{0}remove recommended' or '{0}remove suggestion' ".format(cmd_prefix))

                # CHANGE THE PREFIX
                elif message.content.startswith("{}prefix".format(cmd_prefix)):
                    if len(message.content.split()) == 1:
                        temp_message = await message.channel.send('Please include a prefix')
                        await asyncio.sleep(3)
                        await temp_message.delete()
                    else:
                        new_prefix = message.content.split()[1]
                        if len(new_prefix) > 2:
                            temp_message = await message.channel.send('Prefix should be under two characters long')
                            await asyncio.sleep(3)
                            await temp_message.delete()
                        else:
                            database.set_prefix(server_id, new_prefix)

                # CLEAR THE CHAT
                elif message.content.startswith("{}clear".format(cmd_prefix)):
                    msgs = []
                    if len(message.content.split()) > 1:
                        number = int(message.content.split()[1]) + 1
                    else:
                        number = 6
                    await message.channel.purge(limit = number)

            # IF USER NOT MOD OR IF CHANNEL ID IS IN MONITORED LIST
            if not message.content.startswith(cmd_prefix):
                if message.channel.id in channel_ids:
                    valid_msg = False

                    # CHECK IF USING SUGGESTION PREFIX
                    for prefix in suggestion_prefixs:
                        if message.content.startswith(prefix):
                            await message.add_reaction(yes)
                            await message.add_reaction(no)
                            valid_msg = True

                    # IF NOT USING PREFIX
                    if not valid_msg:
                        if not is_mod:
                            send_channel = message.channel
                            await message.delete() # DELETE THEIR MESSAGE
                            temp_message = await send_channel.send('%s please use [SUBREDDIT], [DISCORD] or [CHH] for your suggestions' % message.author.mention)
                            await asyncio.sleep(5)
                            await temp_message.delete()
            elif message.channel.id in recommended_channel_ids:
                if message.content.startswith("{}recommend".format(cmd_prefix)):
                    search_string = message.content.replace("{}recommend".format(cmd_prefix), "")
                    search_string = search_string.replace(" ", "")
                    if search_string == "":
                        await message.channel.send("%s Please specify an artist name to recommend" % message.author.mention)
                    else:
                        SPOTIPY_ID = os.getenv('SPOTIPY_ID')
                        SPOTIPY_SECRET = OS.getenv('SPOTIPY_SECRET')
                        sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=SPOTIPY_ID, client_secret=SPOTIPY_SECRET))
                        results = sp.search(q=search_string, limit=5, type='artist')
                        items = results['artists']['items']
                        if len(items) > 0:
                            artist = items[0]
                            await message.channel.send(artist['external_urls']['spotify'])




client = chh_bot()
TOKEN=os.getenv('DISCORD_TOKEN')
client.run(TOKEN)
