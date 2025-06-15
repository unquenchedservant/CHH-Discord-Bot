from ctypes import util

import discord
import utilities
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
    "cogs.aprilfools",
    "cogs.birthdays",
    "cogs.events",
    "cogs.selfpromo",
    "cogs.starboard",
]


class Admin(commands.Cog):

    starboardgrp = SlashCommandGroup(guild_ids=utilities.GUILD_ID, name="starboard", description="Starboard commands")
    holidaygrp = SlashCommandGroup(guild_ids=utilities.GUILD_ID, name="holiday", description="Holiday commands")
    rolememgrp = SlashCommandGroup(guild_ids=utilities.GUILD_ID, name="rolememory", description="Role Memory commands")

    def __init__(self, bot):
        self.bot = bot
        self.starboard_settings = StarboardSettings()
        self.holiday = Holiday()
        self.rolememory = RoleMemory()
        self.archival = Archival()

    '''
    Archive command

    Given a channel ID is provided, and no level, sort channel to the initial archive (public viewing, no send msg)
    Given a channel ID is provided, and the level=1, sort channel to the initial archive (public viewing, no send msg)
    Given a channel ID is provided, and the level=2, sort channel to the hidden archive (mods only)
    '''

    @slash_command(
            guild_ids=utilities.GUILD_ID,
            default_permission=False,
            description="Starts the archive process on a given channel"
    )
    async def archive(self, ctx: discord.ApplicationContext, channel: Option(discord.TextChannel, "Channel to be archived", required=True, default=None), level: Option(int, "Level of archive(1 or 2)", default=1)):
        data = self.archival.check(channel.id)
        if data:
            if data[0][3] == level:
                await ctx.respond("That channel has already been set to be archived at that level", ephemeral=True)
            else:
                self.archival.update(channel.id, level)
                # method to update the channel goes here, this will be based on level
        else:
            current_month = datetime.now().month
            current_day = datetime.now().day
            if level == 2:
                current_month = check_month(current_month - 3)
            self.archival.set(channel.id, current_month, current_day, level)




    @slash_command(
        guild_ids=utilities.GUILD_ID,
        default_permission=False,
        description="Used for reloading cogs during development")
    async def reload(self, ctx: discord.ApplicationContext):
        logger.info("reload - User: {}".format(ctx.author.name))
        for extension in EXTENSIONS:
            self.bot.reload_extension(extension)
        await ctx.respond("Cogs have been reloaded!", ephemeral=True)

    """
    =========
    Starboad Management
    =========
    """

    @starboardgrp.command(guild_ids=utilities.GUILD_ID, name="threshold", default_permission=False,description="Set the threshold for the starboard")
    async def setthreshold(self, ctx: discord.ApplicationContext, threshold: int):
        logger.info("starboard - threshold - User: {}".format(ctx.author.name))
        if ctx.author.guild_permissions.kick_members:
            self.starboard_settings.update_threshold(ctx.guild.id, threshold)
            await ctx.respond("Starboard threshold set to {}".format(threshold), ephemeral=True)
        else:
            await ctx.respond(ERROR_MSG, ephemeral=True)

    @starboardgrp.command(guild_ids=utilities.GUILD_ID, name="channel", default_permission=False, description="Set the channel for the starboard")
    async def setchannel(self, ctx: discord.ApplicationContext, channel: discord.TextChannel):
        logger.info("starboard - setchannel - User: {}".format(ctx.author.name))
        if ctx.author.guild_permissions.kick_members:
            self.starboard_settings.update_channel(ctx.guild.id, channel.id)
            await ctx.respond("Starboard channel set to {}".format(channel.name), ephemeral=True)
        else:
            await ctx.respond(ERROR_MSG, ephemeral=True)

    """
    =========
    Holiday Management
    =========
    """

    @holidaygrp.command(
        guild_ids=utilities.GUILD_ID,
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
        if ctx.author.guild_permissions.kick_members:
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
        else:
            await ctx.respond(ERROR_MSG, ephemeral=True)

    @holidaygrp.command(
        guild_ids=utilities.GUILD_ID,
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
        if ctx.author.guild_permissions.kick_members:
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
        else:
            await ctx.respond(ERROR_MSG, ephemeral=True)

    @holidaygrp.command(
        guild_ids=utilities.GUILD_ID,
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
        if ctx.author.guild_permissions.kick_members:
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
        else:
            await ctx.respond(ERROR_MSG, ephemeral=True)

    """
    =========
    Role Memory Management
    =========
    """

    @rolememgrp.command(guild_ids=utilities.GUILD_ID, default_permission=False)
    async def toggle(self, ctx: discord.ApplicationContext):
        logger.info("togglerolememory - User: {}".format(ctx.author.name))
        if ctx.author.guild_permissions.kick_members:
            status = self.rolememory.check(ctx.guild.id)
            msg = ""
            if status == 1:
                msg = "Role memory has been turned off for this server"
            if status == 0:
                msg = "Role memory has been turned on for this server"
            self.rolememory.toggle(ctx.guild.id)
            await ctx.respond(msg, ephemeral=True)
        else:
            await ctx.respond(ERROR_MSG, ephemeral=True)

    @rolememgrp.command(guild_ids=utilities.GUILD_ID, default_permission=False)
    async def check(self, ctx: discord.ApplicationContext):
        logger.info("checkrolememory - User: {}".format(ctx.author.name))
        if ctx.author.guild_permissions.kick_members:
            status = self.rolememory.check(ctx.guild.id)
            msg = ""
            if status == 1:
                msg = "Role memory is turned on on this server"
            else:
                msg = "Role memory is turned off on this server"
            await ctx.respond(msg, ephemeral=True)
        else:
            await ctx.respond(ERROR_MSG, ephemeral=True)


def setup(bot):
    bot.add_cog(Admin(bot))
