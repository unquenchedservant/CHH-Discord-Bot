from ctypes import util

import discord
import utilities
from utilities import Config
from discord.commands import Option, slash_command
from discord.ext import commands
from discord import SlashCommandGroup
from datetime import datetime
from utilities.database import Holiday, StarboardSettings, RoleMemory, Archival
from utilities.logging import logger
from utilities import check_month
ERROR_MSG = "You need to be a mod or admin to use this command"



EXTENSIONS = [
    "cogs.admin",
    "cogs.birthdays",
    "cogs.events",
    "cogs.selfpromo",
    "cogs.starboard",
]


class Admin(commands.Cog):

    starboardgrp = SlashCommandGroup(name="starboard", description="Starboard commands")
    holidaygrp = SlashCommandGroup(name="holiday", description="Holiday commands")
    rolememgrp = SlashCommandGroup(name="rolememory", description="Role Memory commands")
    ROLE_MEMORY_ON_MSG = "Role memory is turned on on this server"
    ROLE_MEMORY_OFF_MSG = "Role memory is turned off on this server"
    HOLIDAY_ERROR_MSG = "Holiday not removed, may not exist"

    async def has_permission(self, ctx):
        if not ctx.author.guild_permissions.kick_members:
            await ctx.respond(ERROR_MSG, ephemeral=True)
            return False
        return True

    def __init__(self, bot):
        self.bot = bot
        self.starboard_settings = StarboardSettings()
        self.holiday = Holiday()
        self.rolememory = RoleMemory()
        self.archival = Archival()
        self.config = Config()

    async def handle_existing_archive(self, channel, level, data):
        if data[0][3] == 2 and level == 1:
            current_month = check_month(datetime.now().month + 6)
            self.archival.update(channel.id, level=level, month=current_month)
        else:
            self.archival.update(channel.id, level=level)
        return None
    
    async def handle_new_archive(self, channel, level):
        current_month = datetime.now().month
        current_day = datetime.now().day
        if level == 2:
            current_month = check_month(current_month - 3)
        self.archival.set(channel.id, current_month, current_day, level)

    async def channel_move(self, channel: discord.channel, level, guild: discord.guild):
        if level == 1:
            new_category_id = self.config.get_archive_1_id()
        elif level == 2:
            new_category_id = self.config.get_archive_2_id()
        category = discord.utils.get(guild.categories, id=new_category_id)
        await channel.move(category=category, sync_permissions=True, beginning=True)
    
    '''
    Archive command

    Given a channel ID is provided, and no level, sort channel to the initial archive (public viewing, no send msg)
    Given a channel ID is provided, and the level=1, sort channel to the initial archive (public viewing, no send msg)
    Given a channel ID is provided, and the level=2, sort channel to the hidden archive (mods only)
    '''
    @slash_command(
            default_permission=False, description="Remove a channel from archiver(database only)"
    )
    async def archive_remove(self, ctx:discord.ApplicationContext, channel: Option(discord.TextChannel, "Channel to be unarchived", required=True, default=None)):
        if not await self.has_permission(ctx):
            return
        self.archival.remove(channel.id)
        await ctx.respond("Successfully removed {} from the DB, please move it manually and sync permissions if applicable".format(channel.name), ephemeral=True)

    @slash_command(
            default_permission=False,
            description="Starts/Updates the archive process on a given channel"
    )
    async def archive(self, ctx: discord.ApplicationContext, channel: Option(discord.TextChannel, "Channel to be archived", required=True, default=None), level: Option(int, "Level of archive(1 or 2)", default=1, min_value=1, max_value=2)): # type: ignore
        if not await self.has_permission(ctx):
            return
    
        data = self.archival.check(channel.id)
        if len(data) > 0:
            if data[0][3] == level:
                await ctx.respond("That channel has already been set to be archived at that level", ephemeral=True)
            else:
                await self.handle_existing_archive(channel, level, data)
                await self.channel_move(channel, level, ctx.guild)
                await ctx.respond("Successfully updated archive level of {} to {}".format(channel.name, level), ephemeral=True)
        else:
            if level < 0 or level > 2: # Level should only be 1 or 2
                await ctx.respond("Please enter a valid level\n 1 - Anyone can view, no messages\n2 - Only mods can view", ephemeral=True)
            else:
                await self.handle_new_archive(channel, level)
                await self.channel_move(channel, level, ctx.guild)
                await ctx.respond("Successfully archived {} at Level {}".format(channel.name, level), ephemeral=True)

    @slash_command(
        default_permission=False,
        description="Used for reloading cogs during development")
    async def reload(self, ctx: discord.ApplicationContext):
        if not await self.has_permission(ctx):
            return
        logger.info("reload - User: {}".format(ctx.author.name))
        for extension in EXTENSIONS:
            self.bot.reload_extension(extension)
        await ctx.respond("Cogs have been reloaded!", ephemeral=True)

    # @slash_command(
    #     default_permission=False,
    #     description="Used to check others birthdays")
    # async def checkbirthday(self, user: Option(discord.User, "User to check birthday", required=True, default=None), ctx: discord.ApplicationContext):
    #     if not await self.has_permission(ctx):
    #         return
    #     birthday = self.birthday.get(user.id)
    #     if birthday == [0, 0]:
    #         await ctx.respond("User does not have a birthday set, use `/setbirthday` to do so", ephemeral=True)
    #     else:
    #         await ctx.respond(f"{user.name} birthday is set to {birthday[0]}/{birthday[1]}", ephemeral=True)


    """
    =========
    Starboad Management
    =========
    """

    @starboardgrp.command( name="threshold", default_permission=False,description="Set the threshold for the starboard")
    async def setthreshold(self, ctx: discord.ApplicationContext, threshold: int):
        logger.info("starboard - threshold - User: {}".format(ctx.author.name))
        if not await self.has_permission(ctx):
            return
        self.starboard_settings.update_threshold(ctx.guild.id, threshold)
        await ctx.respond("Starboard threshold set to {}".format(threshold), ephemeral=True)

    @starboardgrp.command( name="channel", default_permission=False, description="Set the channel for the starboard")
    async def setchannel(self, ctx: discord.ApplicationContext, channel: discord.TextChannel):
        logger.info("starboard - setchannel - User: {}".format(ctx.author.name))
        if not await self.has_permission(ctx):
            return
        self.starboard_settings.update_channel(ctx.guild.id, channel.id)
        await ctx.respond("Starboard channel set to {}".format(channel.name), ephemeral=True)
        

    """
    =========
    Holiday Management
    =========
    """

    @holidaygrp.command(
        
        default_permission=False,
        description="Used to add/update an automated holiday message",
    )
    async def add(
        self,
        ctx: discord.ApplicationContext,
        month: Option(
            int,
            "Enter the Month (1-12) this holiday occurs",
            min_value=1,
            max_value=12,
            required=True,
        ), # type: ignore
        day: Option(
            int,
            "Enter the day(1-31) this holiday occurs",
            min_value=1,
            max_value=31,
            required=True,
        ), # type: ignore
        msg: Option(
            str, "What message would you like to send on this day", required=True
        ), # type: ignore
    ):
        logger.info("addholiday - User: {}".format(ctx.author.name))
        if not await self.has_permission(ctx):
            return
        if not month:
            await ctx.respond(
                "Please enter the holiday month (1-12)", ephemeral=True
            )
        elif not day:
            await ctx.respond("Please enter the holiday day (1-31)", ephemeral=True)
        elif not msg:
            await ctx.respond("Please enter a holiday message", ephemeral=True)
        else:
            updated = self.holiday.add(month, day, msg)
            month = utilities.zero_leading(month)
            day = utilities.zero_leading(day)
            if updated:
                response_msg = "Successfully updated holiday message on {}/{} with the message: {}".format(
                    month, day, msg
                )
            else:
                response_msg = "Successfully saved a new holiday on {}/{} with the message: {}".format(
                    month, day, msg
                )
            await ctx.respond(response_msg)
        

    @holidaygrp.command(
        
        default_permission=False,
        description="Check if a given holiday exists",
    )
    async def check(
        self,
        ctx: discord.ApplicationContext,
        month: Option(
            int,
            "Enter the month (1-12) you'd like to check",
            min_value=1,
            max_value=12,
            required=False,
        ), # type: ignore
        day: Option(
            int,
            "Enter the day (0-31) you'd like to check",
            min_value=1,
            max_value=31,
            required=False,
        ), # type: ignore
    ):
        logger.info("checkholiday - User: {}".format(ctx.author.name))
        if not await self.has_permission(ctx):
            return
        if not month and not day:
            logger.info("checkholidays - User: {}".format(ctx.author.name))
            if ctx.author.guild_permissions.kick_members:
                msg = ""
                holidays = self.holiday.check_multi()
                if len(holidays) == 0:
                    msg = "No holidays set"
                else:
                    for item in holidays:
                        month, day, message = item
                        month = utilities.zero_leading(month)
                        day = utilities.zero_leading(day)
                        msg = msg + "{}/{} - {}\n\n".format(month, day, message)
                await ctx.respond(msg)
            else:
                await ctx.respond(ERROR_MSG, ephemeral=True)
        elif not month:
            await ctx.respond(
                "Please enter the holiday month (1-12)", ephemeral=True
            )
        elif not day:
            await ctx.respond("Please enter the holiday day (1-31)", ephemeral=True)
        else:
            msg = self.holiday.check(month, day)
            if msg == 0:
                await ctx.respond("There is no holiday on that day", ephemeral=True)
            else:
                month = utilities.zero_leading(month)
                day = utilities.zero_leading(day)
                await ctx.respond(
                    "The message for {}/{} is : {}".format(month, day, msg),
                    ephemeral=True,
                )
        msg = self.holiday.checkHoliday(month, day)

    @holidaygrp.command(
        
        default_permission=False,
        description="Removes a given holiday from the automation",
    )
    async def remove(
        self,
        ctx: discord.ApplicationContext,
        month: Option(
            int,
            "Enter the month (1-12) this holiday occurs",
            min_value=1,
            max_value=12,
            required=True,
        ), # type: ignore
        day: Option(
            int,
            "Enter the day (1-31) this holiday occurs",
            min_value=1,
            max_value=31,
            required=True,
        ), # type: ignore
    ):
        logger.info("removeholiday - User: {}".format(ctx.author.name))
        if not await self.has_permission(ctx):
            return
        if not month:
            await ctx.respond(
                "Please enter the holiday month (1-12)", ephemeral=True
            )
        elif not day:
            await ctx.respond("Please enter the holiday day (1-31)", ephemeral=True)
        else:
            status = self.holiday.remove(month, day)
            if status == 1:
                month = utilities.zero_leading(month)
                day = utilities.zero_leading(day)
                await ctx.respond(
                    "Holiday on {}/{} removed".format(month, day), ephemeral=True
                )
            elif status == 0:
                await ctx.respond(
                    "Holiday not removed, may not exist", ephemeral=True
                )

    """
    =========
    Role Memory Management
    =========
    """

    @rolememgrp.command( default_permission=False)
    async def toggle(self, ctx: discord.ApplicationContext):
        logger.info("togglerolememory - User: {}".format(ctx.author.name))
        if not await self.has_permission(ctx):
            return
        status = self.rolememory.check(ctx.guild.id)
        msg = ""
        if status == 1:
            msg = "Role memory has been turned off for this server"
        if status == 0:
            msg = "Role memory has been turned on for this server"
        self.rolememory.toggle(ctx.guild.id)
        await ctx.respond(msg, ephemeral=True)

    @rolememgrp.command( default_permission=False)
    async def check(self, ctx: discord.ApplicationContext):
        logger.info("checkrolememory - User: {}".format(ctx.author.name))
        if not await self.has_permission(ctx):
            return
        status = self.rolememory.check(ctx.guild.id)
        msg = ""
        if status == 1:
            msg = "Role memory is turned on on this server"
        else:
            msg = "Role memory is turned off on this server"
        await ctx.respond(msg, ephemeral=True)


def setup(bot):
    bot.add_cog(Admin(bot))
