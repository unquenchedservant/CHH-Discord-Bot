from discord.ext import commands
import utilities
from datetime import time, timezone, datetime
from dateutil.relativedelta import relativedelta
from discord.ext import tasks
from utilities.database import Birthday, Holiday, Archival
from utilities.logging import logger
import random

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.birthday = Birthday()
        self.holiday = Holiday()

        self.daily_birthday_task.start()
        self.daily_holiday_task.start()
        self.one_one_six.start()
        self.archive_check.start()

    @tasks.loop(time=time(5,0, tzinfo=timezone.utc))
    async def archive_check(self):
        pass


    @tasks.loop(time=time(13, 0, tzinfo=timezone.utc))
    async def daily_birthday_task(self):
        """
        A scheduled task that runs daily at 13:00 UTC (08:00 ET) to check for birthdays.

        This task queries the database for users whose birthdays match the current
        date (month and day). If any birthdays are found, it constructs a message
        tagging the users and sends it to the announcements channel.

        Steps:
        1. Retrieve the current month and day.
        2. Query the database for user IDs with birthdays on the current date.
        3. If birthdays are found:
           - Construct a message tagging the users.
           - Append a note encouraging others to set their birthdays.
           - Send the message to the announcements channel.

        Notes:
        - The announcements channel ID is retrieved from the `utilities` module.
        - The task logs the list of user IDs found for debugging purposes.

        Exceptions:
        - Any exceptions during the database query or message sending will propagate.

        Returns:
        None
        """
        current_month = datetime.now().month
        current_day = datetime.now().day
        birthday_ids = self.birthday.check(current_month, current_day)
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
        """
        A scheduled task that runs daily at 05:00 UTC (00:00 ET) to check for holidays.

        This task queries the database for holidays that match the current
        date (month and day). If a holiday message is found, it sends the
        message to the announcements channel, except on January 16th.

        Steps:
        1. Retrieve the current month and day.
        2. Query the database for a holiday message corresponding to the current date.
        3. If a holiday message is found and the date is not January 16th:
           - Send the holiday message to the announcements channel.

        Notes:
        - The announcements channel ID is retrieved from the `utilities` module.
        - January 16th is excluded because it is handled by the `one_one_six` task.

        Exceptions:
        - Any exceptions during the database query or message sending will propagate.

        Returns:
        None
        """
        current_month = datetime.now().month
        current_day = datetime.now().day
        holiday_message = self.holiday.check(current_month, current_day)
        if holiday_message and not (current_month == 1 and current_day == 16):
            channel = self.bot.get_channel(utilities.ANNOUNCEMENTS_CHANNEL_ID)
            await channel.send(holiday_message)

    @tasks.loop(time=time(18,16,tzinfo=timezone.utc))
    async def one_one_six(self):
        """
        A scheduled task that runs daily at 18:16 UTC (13:16 ET) to celebrate January 16th (1/16).

        This task checks if the current date is January 16th. If it is, it retrieves
        a holiday message for January 16th from the database. If no message is found,
        it sends a default celebratory message to the announcements channel.

        Steps:
        1. Retrieve the current month and day.
        2. Check if the current date is January 16th.
        3. If it is January 16th:
           - Query the database for a holiday message for January 16th.
           - If no message is found, use a default celebratory message.
           - Send the message to the announcements channel.

        Notes:
        - The announcements channel ID is retrieved from the `utilities` module.
        - This task is specifically designed to handle January 16th celebrations.

        Exceptions:
        - Any exceptions during the database query or message sending will propagate.

        Returns:
        None
        """
        logger.info("")
        current_month = datetime.now().month
        current_day = datetime.now().day
        if current_month == 1 and current_day == 16:
            channel = self.bot.get_channel(utilities.ANNOUNCEMENTS_CHANNEL_ID)
            msg = self.holiday.check(1,16)
            if not msg:
                msg = "LET ME HEAR YOU SHOUT 1 1 6!\n\n Happy 116 day, everyone!"
            await channel.send(msg)

def setup(bot):
    bot.add_cog(Events(bot))