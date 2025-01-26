from ctypes import util
import discord
from discord.commands import (slash_command)
from discord.commands import Option
from discord.ext import commands
from utilities import database
import utilities
ERROR_MSG = "You need to be a mod or admin to use this command"
GUILD_ID=utilities.get_guild_ids(False)
class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    '''
    =========
    Holiday Management
    =========
    '''
    @slash_command(guild_ids=GUILD_ID, default_permission=False)
    async def addholiday(self, 
        ctx: discord.ApplicationContext,
        month: Option(int, "Enter the Month (1-12) this holiday occurs", min_value=1, max_value=12, required=True),
        day: Option(int, "Enter the day(1-31) this holiday occurs", min_value=1, max_value=31, required=True),
        msg: Option(str, "What message would you like to send on this day", required=True)):
        if ctx.author.guild_permissions.kick_members:
            if not month:
                await ctx.respond("Please enter the holiday month (1-12)", ephemeral=True)
            elif not day:
                await ctx.respond("Please enter the holiday day (1-31)", ephemeral=True)
            elif not msg: 
                await ctx.respond("Please enter a holiday message", ephemeral=True)
            else:
                database.addHoliday(month, day, msg)
                await ctx.respond("Successfully saved a new holiday on {}-{} with the msg: {}".format(month,day, msg))
        else:
            await ctx.respond(ERROR_MSG, ephemeral=True)

    @slash_command(guild_ids=GUILD_ID, default_permission=False) 
    async def checkholiday(self,
        ctx:discord.ApplicationContext,
        month: Option(int, "Enter the month (1-12) you'd like to check", min_value=1, max_value=12, required=True),
        day: Option(int, "Enter the day (0-31) you'd like to check", min_value=1, max_value=31, required=True)):
        if ctx.author.guild_permissions.kick_members:
            if not month:
                await ctx.respond("Please enter the holiday month (1-12)", ephemeral=True)
            elif not day:
                await ctx.respond("Please enter the holiday day (1-31)", ephemeral=True)
            else:
                msg = database.checkHoliday(month, day)
                if msg == 0:
                    await ctx.respond("There is no holiday on that day", ephemeral=True)
                else:
                    await ctx.respond("The message for {}/{} is : {}".format(month, day, msg), ephemeral=True)
            msg = database.checkHoliday(month, day)
        else:
            await ctx.respond(ERROR_MSG, ephemeral=True)

    @slash_command(guild_ids=GUILD_ID, default_permission=False)
    async def checkholidays(self, ctx: discord.ApplicationContext):
        if ctx.author.guild_permissions.kick_members:
            msg = ""
            holidays = database.checkHolidays()
            if len(holidays) == 0:
                msg = "No holidays set"
            else:
                for item in holidays:
                    month, day, message = item
                    if month < 10:
                        month = "0{}".format(month)
                    if day < 10:
                        day = "0{}".format(day)
                    msg = msg + "{}/{} - {}\n\n".format(month,day,message)
            await ctx.respond(msg, ephemeral=True)
        else:
            await ctx.respond(ERROR_MSG, ephemeral=True)

    @slash_command(guild_ids=GUILD_ID, default_permission=False)
    async def removeholiday(self,
        ctx: discord.ApplicationContext,
        month: Option(int, "Enter the month (1-12) this holiday occurs", min_value=1, max_value=12, required=True),
        day: Option(int, "Enter the day (1-31) this holiday occurs", min_value=1, max_value=31, required=True)):
        if ctx.author.guild_permissions.kick_members:
            if not month:
                await ctx.respond("Please enter the holiday month (1-12)", ephemeral=True)
            elif not day:
                await ctx.respond("Please enter the holiday day (1-31)", ephemeral=True)
            else:
                status = database.removeHoliday(month,day)
                if status == 1:
                    await ctx.respond("Holiday removed", ephemeral=True)
                elif status == 0:
                    await ctx.respond("Holiday not removed, may not exist", ephemeral=True)
        else:
            await ctx.respond(ERROR_MSG, ephemeral=True)

    """
    =========
    Role Memory Management
    =========
    """
    @slash_command(guild_ids=GUILD_ID, default_permission=False)
    async def togglerolememory(self, ctx: discord.ApplicationContext):
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
    
    @slash_command(guild_ids=GUILD_ID, default_permission=False)
    async def checkrolememory(self, ctx: discord.ApplicationContext):
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