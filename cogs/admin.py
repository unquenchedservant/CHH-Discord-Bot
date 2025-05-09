from ctypes import util

import discord
import utilities
from discord.commands import Option, slash_command
from discord.ext import commands
from discord import SlashCommandGroup
from utilities import database
from utilities.logging import logger

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
            database.updateStarboardThreshold(ctx.guild.id, threshold)
            await ctx.respond("Starboard threshold set to {}".format(threshold), ephemeral=True)
        else:
            await ctx.respond(ERROR_MSG, ephemeral=True)

    @starboardgrp.command(guild_ids=utilities.GUILD_ID, name="channel", default_permission=False, description="Set the channel for the starboard")
    async def setchannel(self, ctx: discord.ApplicationContext, channel: discord.TextChannel):
        logger.info("starboard - setchannel - User: {}".format(ctx.author.name))
        if ctx.author.guild_permissions.kick_members:
            database.updateStarboardChannel(ctx.guild.id, channel.id)
            await ctx.respond("Starboard channel set to {}".format(channel.name), ephemeral=True)
        else:
            await ctx.respond(ERROR_MSG, ephemeral=True)

    """
    =========
    Database Management
    =========
    
    @slash_command(guild_ids=utilities.GUILD_ID, default_permission=False, description="Updates a database, assumes function modified")
    async def updatedb(self, ctx: discord.ApplicationContext):
        database.updateDB()
        await ctx.respond("Updated DB", ephemeral=True)
    """
    """
    =========
    Birthday Management
    =========
    @slash_command(guild_ids=utilities.GUILD_ID, default_permission=False, description="To run through the database once and clear any inactive users")
    async def clearbirthdays(self, ctx: discord.ApplicationContext):
        active_ids = []
        updated_ids = []
        response = ""
        for guild in self.bot.guilds:
            if guild.id == GUILD_ID[0]:
                for member in guild.members:
                    active_ids.append(member.id)
        all_ids = database.getBirthdays()
        for ind_id in all_ids:
            if not ind_id in active_ids:
                database.setBirthdayActive(False, ind_id)
                response = response + ind_id + "\n"
        ctx.respond("Set the following IDs to inactive:\n\n" + response, ephemeral=True)
    """
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
                updated = database.addHoliday(month, day, msg)
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
                    holidays = database.checkHolidays()
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
                msg = database.checkHoliday(month, day)
                if msg == 0:
                    await ctx.respond("There is no holiday on that day", ephemeral=True)
                else:
                    month = utilities.zero_leading(month)
                    day = utilities.zero_leading(day)
                    await ctx.respond(
                        "The message for {}/{} is : {}".format(month, day, msg),
                        ephemeral=True,
                    )
            msg = database.checkHoliday(month, day)
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
                status = database.removeHoliday(month, day)
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
            status = database.checkRoleMemory(ctx.guild.id)
            msg = ""
            if status == 1:
                msg = "Role memory has been turned off for this server"
            if status == 0:
                msg = "Role memory has been turned on for this server"
            database.toggleRoleMemory(ctx.guild.id)
            await ctx.respond(msg, ephemeral=True)
        else:
            await ctx.respond(ERROR_MSG, ephemeral=True)

    @rolememgrp.command(guild_ids=utilities.GUILD_ID, default_permission=False)
    async def check(self, ctx: discord.ApplicationContext):
        logger.info("checkrolememory - User: {}".format(ctx.author.name))
        if ctx.author.guild_permissions.kick_members:
            status = database.checkRoleMemory(ctx.guild.id)
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
