import discord
from discord.commands import (slash_command)
from discord.commands import Option
from discord import option
from discord.ext import commands
from utilities import database
import utilities
from datetime import time, timezone, datetime
from discord.ext import tasks

ERROR_MSG = "You need to be a mod or admin to use this command"
GUILD_ID=utilities.get_guild_ids(utilities.get_is_dev())

if utilities.get_is_dev():
    BROADCAST_CHANNEL = 471397276468903936
else:
    BROADCAST_CHANNEL = 613469111682334762

class Birthdays(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.daily_birthday_task.start()
        self.daily_holiday_task.start()
        self.one_one_six.start()

    @slash_command(guild_ids=GUILD_ID, description="Set your birthday on the server to get a shout-out!")    
    async def setbirthday(
        self, 
        ctx: discord.ApplicationContext, 
        month: Option(int, "Enter your birth month", min_value=1, max_value=12, required=True), 
        day: Option(int, "Enter your birth date", min_value=1, max_value=31, required=True)
    ):
        if not month:
            await ctx.respond("Please enter your birth month (1-12)")
        elif not day:
            await ctx.respond("Please enter your birth date (1-31)")
        else:
            database.setBirthday(ctx.author.id, month, day) 
            await ctx.respond("Your birthday has been set successfully", ephemeral=True)

    @slash_command(guild_ids=GUILD_ID, description="Check to make sure you have your birthday set correctly")
    async def getbirthday(self, ctx: discord.ApplicationContext):
        birthday = database.getBirthday(ctx.author.id)
        if birthday == [0, 0]:
            await ctx.respond("You do not have a birthday set, use `/setbirthday` to do so", ephemeral=True)
        else:
            await ctx.respond("Your birthday is set to {}/{}".format(birthday[0], birthday[1]), ephemeral=True)

    @slash_command(guild_ids=GUILD_ID, description="Removes you from our birthday list")
    async def removebirthday(self, ctx: discord.ApplicationContext):
        database.removeBirthday(ctx.author.id)
        await ctx.respond("Your birthday has been removed successfully", ephemeral=True)

    @tasks.loop(time=time(13, 0, tzinfo=timezone.utc))
    async def daily_birthday_task(self):
        current_month = datetime.now().month
        current_day = datetime.now().day
        birthday_ids = database.checkBirthday(current_month, current_day)
        msg = "We've got a birthday! Make sure to wish the following people a happy birthday:\n\n"
        for id in birthday_ids:
            msg = msg + "<@" + str(id) + ">\n"
        channel_id = BROADCAST_CHANNEL 
        if not len(birthday_ids) == 0:
            channel = self.bot.get_channel(BROADCAST_CHANNEL)
            await channel.send(msg)

    @tasks.loop(time=time(5,0,tzinfo=timezone.utc))
    async def daily_holiday_task(self):
        current_month = datetime.now().month
        current_day = datetime.now().day
        holiday_message = database.checkHoliday(current_month, current_day)
        if holiday_message and not (current_month == 1 and current_day == 16):
            channel = self.bot.get_channel(BROADCAST_CHANNEL)
            await channel.send(holiday_message)

    @tasks.loop(time=time(18,16,tzinfo=timezone.utc))
    async def one_one_six(self):
        current_month = datetime.now().month
        current_day = datetime.now().day
        if current_month == 1 and current_day == 16:
            channel = self.bot.get_channel(BROADCAST_CHANNEL)
            msg = database.checkHoliday(1,16)
            if not msg:
                msg = "LET ME HEAR YOU SHOUT 1 1 6!\n\n Happy 116 day, everyone!"
            await channel.send(msg)
        
def setup(bot):
    bot.add_cog(Birthdays(bot))