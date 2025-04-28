from discord.ext import commands
import utilities
from utilities.logging import logger
from utilities import database
import discord
import pytz
import asyncio

DEBUG=utilities.is_dev

"""
==========
Starboard
==========

Starboard cog mimicks functionality of starboard in other popular apps, while greatly copying, this is reverse engineered, and not a direct copy of any code.
"""

class Starboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.lock = asyncio.Lock()

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
    async def get_true_count(self, msg):
        true_count = 0
        for reaction in msg.reactions:
            if reaction.emoji == "⭐":
                if not DEBUG:
                    logger.info("")
                    users = [user async for user in reaction.users()]
                    for user in users:
                        if user.bot:
                            logger.debug("Starboard - Bot reacts don't count")
                        if not user.id == msg.author.id:
                            if reaction.emoji == "⭐":
                                true_count += 1
                else:
                    true_count = reaction.count
        return true_count

    # Listens for reactions on messages, checks if it's a star, and if it is, verifies if it has enough stars to be posted to the starboad
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        async with self.lock:
            true_count = 0
            if payload.emoji.name == "⭐":
                msg = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
                true_count = await self.get_true_count(msg)
                onModBoard = database.checkModboard(payload.message_id)
                if true_count >= database.getStarboardThreshold(utilities.GUILD_ID):
                    if onModBoard:
                        modboardID = database.getModboardMessage(payload.message_id)
                        modboardMSG = await self.bot.get_channel(utilities.MODBOARD_CHANNEL_ID).fetch_message(modboardID)
                        await modboardMSG.delete()
                        database.removeModboard(payload.message_id)
                    starboard = self.bot.get_channel(utilities.STARBOARD_CHANNEL_ID)
                    if not database.checkStarboard(payload.message_id):
                        embed = self.create_embed(msg, true_count)
                        strbrdmsg = await starboard.send(embed=embed)
                        database.addStarboard(payload.message_id, strbrdmsg.id)
                    else:
                        embed = self.create_embed(msg, true_count)
                        starboard_msg_id = database.getStarboardMessage(payload.message_id)
                        starboard_msg = await self.bot.get_channel(utilities.STARBOARD_CHANNEL_ID).fetch_message(starboard_msg_id)
                        await starboard_msg.edit(embed=embed)
                else:
                    modboard_channel_id = utilities.MODBOARD_CHANNEL_ID
                    modboard = self.bot.get_channel(modboard_channel_id)
                    onModBoard = database.checkModboard(payload.message_id)
                    mod_count = await self.get_mod_count(msg)
                    if len(mod_count) > 0:
                        modboard_embed = self.create_mod_embed(msg, mod_count[0])
                        modboardMsg = await modboard.send(embed=modboard_embed)
                        database.addModboard(payload.message_id, modboardMsg.id)

    # Listens for reactions being removed from messages, checks if it's a star, and if it is, verifies if it has enough stars to be posted to the starboad
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        logger.debug("Starboard - Reaction removed start")        
        async with self.lock:
            true_count = 0
            logger.debug("Starboard - Reaction removed start in async")
            if payload.emoji.name == "⭐":
                logger.info("Starboard - Star removed")
                logger.debug("Starboard - Reaction removed is a star")
                msg = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
                modboard_channel_id = utilities.MODBOARD_CHANNEL_ID
                modboard = self.bot.get_channel(modboard_channel_id)
                onModBoard = database.checkModboard(payload.message_id)
                mod_count = await self.get_mod_count(msg)
                if len(mod_count) == 0:
                    modboardID = database.getModboardMessage(payload.message_id)
                    modboardMSG = await self.bot.get_channel(utilities.MODBOARD_CHANNEL_ID).fetch_message(modboardID)
                    await modboardMSG.delete()
                    database.removeModboard(payload.message_id)
                true_count = await self.get_true_count(msg)
                if true_count < database.getStarboardThreshold(utilities.GUILD_ID):
                    logger.info("Starboard - True count is less than threshold")
                    if database.checkStarboard(payload.message_id):
                        logger.debug("Starboard - Starboard entry exists")
                        starboard_msg_id = database.getStarboardMessage(payload.message_id)
                        starboard_msg = await self.bot.get_channel(utilities.STARBOARD_CHANNEL_ID).fetch_message(starboard_msg_id)
                        await starboard_msg.delete()
                        database.removeStarboard(payload.message_id)
                        logger.info("Starboard - Starboard entry removed")
                        if len(mod_count) > 0:
                            modboard_embed = self.create_mod_embed(msg, mod_count[0])
                            modboardMsg = await modboard.send(embed=modboard_embed)
                            database.addModboard(payload.message_id, modboardMsg.id)
                else:
                    embed = self.create_embed(msg, true_count)
                    starboard_msg_id = database.getStarboardMessage(payload.message_id)
                    starboard_msg = await self.bot.get_channel(utilities.STARBOARD_CHANNEL_ID).fetch_message(starboard_msg_id)
                    await starboard_msg.edit(embed=embed)
                    logger.info("Starboard - Starboard message edited")
            if true_count == 0 and database.checkStarboard(payload.message_id):
                starboard_msg_id = database.getStarboardMessage(payload.message_id)
                starboard_msg = await self.bot.get_channel(utilities.STARBOARD_CHANNEL_ID).fetch_message(starboard_msg_id)
                await starboard_msg.delete()
                database.removeStarboard(payload.message_id)
                logger.info("Starboard - Starboard entry removed")

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
        footer = "Originally ⭐ by {} in #{}".format(user,message.channel.name, utcdate)
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
