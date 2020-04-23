import os, discord, asyncio, sqlite3
from discord.ext import commands
from dotenv import load_dotenv
from utilities import database
load_dotenv()

class chh_bot(discord.Client):

    async def on_ready(self):
        print("Logged on as {0}!".format(self.user))

    async def on_message(self, message):
        yes = "\U00002705"
        no = "\U0001F6AB"

        server_id = message.guild.id

        if not os.path.exists("chh.db"):
            database.create_table()
            database.add_server(server_id, "&")

        cmd_prefix = database.get_prefix(server_id)

        if cmd_prefix == "&":
            database.set_prefix(server_id, "^")
            cmd_prefix = "^"

        channel_ids = database.get_allowed_channels()

        suggestion_prefixs = ["[SUBREDDIT]","[DISCORD]","[CHH]"]

        is_mod = False

        for r in message.author.roles:
            for p in r.permissions:
                if p[0] == "administrator" and p[1] == True:
                    is_mod = True

        if message.author == self.user:
            return
        # START MOD COMMANDS
        if is_mod:
            # ADD CHANNEL TO MONITORING
            if message.content.startswith("{}add".format(cmd_prefix)):
                database.add_channels(message.channel.id)
                temp_message = await message.channel.send('Added this channel to monitored channels')
                await message.delete()
                await asyncio.sleep(3)
                await temp_message.delete()

            # REMOVE CHANNEL FROM MONITORING
            elif message.content.startswith("{}remove".format(cmd_prefix)):
                database.remove_channel(message.channel.id)
                temp_message = await message.channel.send('No longer monitoring this channel')
                await message.delete()
                await asyncio.sleep(3)
                await temp_message.delete()

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
        elif not is_mod or message.channel.id in channel_ids:

            # IF CHANNEL MONITORED
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



client = chh_bot()
TOKEN=os.getenv('DISCORD_TOKEN')
client.run(TOKEN)
