from discord.ext import commands
import utilities
from datetime import time, timezone, datetime
from discord.ext import tasks
from utilities import database
from utilities.logging import logger
import random

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.daily_birthday_task.start()
        self.daily_holiday_task.start()
        self.one_one_six.start()

    @tasks.loop(time=time(13, 0, tzinfo=timezone.utc))
    async def daily_birthday_task(self):
        current_month = datetime.now().month
        current_day = datetime.now().day
        birthday_ids = database.checkBirthday(current_month, current_day)
        logger.info("birthday check 2: {}".format(birthday_ids))
        if not len(birthday_ids) == 0:
            msg = "We've got a birthday! Make sure to wish the following people a happy birthday:\n"
            for id in birthday_ids:
                msg = msg + "<@" + str(id) + ">\n"
            msg = msg + "\nWant a message for your birthday? Use `/birthday set`" 
            channel = self.bot.get_channel(utilities.ANNOUNCEMENTS_CHANNEL_ID)
            await channel.send(msg)

    @tasks.loop(time=time(5,0,tzinfo=timezone.utc))
    async def daily_holiday_task(self):
        current_month = datetime.now().month
        current_day = datetime.now().day
        holiday_message = database.checkHoliday(current_month, current_day)
        if holiday_message and not (current_month == 1 and current_day == 16):
            channel = self.bot.get_channel(utilities.ANNOUNCEMENTS_CHANNEL_ID)
            await channel.send(holiday_message)

    @tasks.loop(time=time(18,16,tzinfo=timezone.utc))
    async def one_one_six(self):
        logger.info("")
        current_month = datetime.now().month
        current_day = datetime.now().day
        if current_month == 1 and current_day == 16:
            channel = self.bot.get_channel(utilities.ANNOUNCEMENTS_CHANNEL_ID)
            msg = database.checkHoliday(1,16)
            if not msg:
                msg = "LET ME HEAR YOU SHOUT 1 1 6!\n\n Happy 116 day, everyone!"
            await channel.send(msg)

def setup(bot):
    bot.add_cog(Events(bot))