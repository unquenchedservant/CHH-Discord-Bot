from discord.ext import commands
from utilities import Config
from utilities.logging import logger
from utilities.database import StarboardDB, Modboard, StarboardSettings
import discord
import pytz
import asyncio

"""
==========
Starboard
==========

Starboard cog mimicks functionality of starboard in other popular apps, while greatly copying, this is reverse engineered, and not a direct copy of any code.
"""

class Starboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config()
        self.lock = asyncio.Lock()
        self.starboard_db = StarboardDB()
        self.modboard = Modboard()
        self.starboard_settings = StarboardSettings()

    async def add_to_starboard(self, msg, true_count, starboard_channel):
        embed = self.create_embed(msg, true_count)
        starboard_msg = await starboard_channel.send(embed=embed)
        self.starboard_db.add(msg.id, starboard_msg.id)

    async def update_starboard(self, msg, true_count, starboard_channel):
        starboard_msg = await starboard_channel.fetch_message(self.starboard_db.get(msg.id))
        embed = self.create_embed(msg, true_count)
        await starboard_msg.edit(embed=embed)

    async def remove_from_starboard(self, msg, starboard_channel):
        starboard_msg = await starboard_channel.fetch_message(self.starboard_db.get(msg.id))
        await starboard_msg.delete()
        self.starboard_db.remove(msg.id)

    async def handle_modboard(self, msg, mod_count, payload):
        modboard_channel_id = self.config.get_modboard_channel()
        modboard = self.bot.get_channel(modboard_channel_id)
        on_modboard = self.modboard.check(payload.message_id)
        true_count = await self.get_true_count(msg)
        if on_modboard:
            modboard_msg_id = self.modboard.get(payload.message_id)
            modboard_msg = await modboard.fetch_message(modboard_msg_id)
            
        if len(mod_count) > 0 and true_count < self.starboard_settings.get_threshold():
            if not on_modboard:
                modboard_embed = self.create_mod_embed(msg, len(mod_count))
                modboard_msg = await modboard.send(embed=modboard_embed)
                self.modboard.add(payload.message_id, modboard_msg.id)
            else:
                modboard_embed = self.create_mod_embed(msg, len(mod_count))
                await modboard_msg.edit(embed=modboard_embed)
        elif on_modboard:
            await modboard_msg.delete()
            self.modboard.remove(payload.message_id)

    async def get_mod_count(self, msg):
        payload = []
        for reaction in msg.reactions:
            if reaction.emoji == "⭐":
                users = [user async for user in reaction.users()]
                for user in users:
                    if user.guild_permissions.manage_channels:
                        if not user.id == msg.author.id:
                            payload.append(user)
        return payload

    # Get the true count of stars on a message (ignores bot reactions and the user who posted the message)
    async def get_true_count(self, msg: discord.Message) -> int:
        true_count = 0
        for reaction in msg.reactions:
            if reaction.emoji == "⭐" and not self.config.is_dev:
                if not self.config.is_dev:
                    logger.info("")
                    users = [user async for user in reaction.users()]
                    true_count = sum(1 for user in users if not user.bot and user.id != msg.author.id)
                else:
                    true_count = reaction.count
        return true_count

    # Listens for reactions on messages, checks if it's a star, and if it is, verifies if it has enough stars to be posted to the starboad
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        async with self.lock:
            if payload.emoji.name == "⭐":
                msg = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
                true_count = await self.get_true_count(msg)
                mod_count = await self.get_mod_count(msg)

                await self.handle_modboard(msg, mod_count, payload)
                
                if true_count >= self.starboard_settings.get_threshold(self.config.get_guild_id()):
                    starboard_channel = self.bot.get_channel(self.config.get_starboard_channel())
                    if not self.starboard_db.check(payload.message_id):
                        await self.add_to_starboard(msg, true_count, starboard_channel)
                    else:
                        await self.update_starboard(msg, true_count, starboard_channel)

    # Listens for reactions being removed from messages, checks if it's a star, and if it is, verifies if it has enough stars to be posted to the starboad
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        async with self.lock:
            if payload.emoji.name == "⭐":
                msg = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)                
                mod_count = await self.get_mod_count(msg)
                self.handle_modboard(msg, mod_count, payload)
                true_count = await self.get_true_count(msg)
                starboard_channel = self.bot.get_channel(self.config.get_starboard_channel())
                if true_count < self.starboard_settings.get_threshold(self.config.get_guild_id()):
                    if self.starboard_db.check(payload.message_id):
                        await self.remove_from_starboard(msg, starboard_channel)
                else:
                    await self.update_starboard(msg, true_count)


    # Creates the embed for the starboard message based on most up to date information. 
    def create_embed(self, message, count):
        author = message.author
        authorName = author.display_name
        authorUser = author.name
        msg = message.content
        msg = msg + "\n\n[⤴️ Go to message]({})".format(message.jump_url)
        utcdate = message.created_at.timestamp()
        utcdate = int(str(utcdate).split(".")[0])
        footer = "⭐ {} in #{}".format(count,message.channel.name, utcdate)
        embed = discord.Embed(description=msg)
        title = ""
        if authorName == authorUser:
            title = authorName
        else:
            title = "{} ~ {}".format(authorUser, authorName)
        embed.set_author(name=title, icon_url=message.author.display_avatar.url)
        embed.set_footer(text=footer)
        embed.timestamp = message.created_at
        if message.attachments:
            if message.attachments[0].content_type.startswith("image"):
                embed.set_image(url=message.attachments[0].url)

        return embed

    def create_mod_embed(self, message, user):
        author = message.author
        authorName = author.display_name
        authorUser = author.name
        msg = message.content
        msg = msg + "\n\n[⤴️ Go to message]({})".format(message.jump_url)
        utcdate = message.created_at.timestamp()
        utcdate = int(str(utcdate).split(".")[0])
        footer = "⭐ by {} mod(s) in #{}".format(user,message.channel.name)
        embed = discord.Embed(description=msg)
        title = ""
        if authorName == authorUser:
            title = authorName
        else:
            title = "{} ~ {}".format(authorUser, authorName)
        embed.set_author(name=title, icon_url=message.author.display_avatar.url)
        embed.set_footer(text=footer)
        embed.timestamp = message.created_at
        if message.attachments:
            if message.attachments[0].content_type.startswith("image"):
                embed.set_image(url=message.attachments[0].url)

        return embed       
         
def setup(bot):
    bot.add_cog(Starboard(bot))
