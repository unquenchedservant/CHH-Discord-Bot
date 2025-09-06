from discord.ext import commands
import utilities
from utilities import Config
from datetime import time, timezone, datetime, date
from discord.ext import tasks
import random
from utilities.database import Birthday, Holiday, Archival
from utilities.logging import logger
import discord
from datetime import datetime, timedelta
from collections import defaultdict
from utilities import openai

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config()
        self.birthday = Birthday()
        self.holiday = Holiday()
        self.archive_db = Archival()

        self.daily_birthday_task.start()
        self.daily_holiday_task.start()
        self.one_one_six.start()
        self.archive_check.start()
        self.ben_last_sent = defaultdict(lambda: datetime.min)
        self.socks_last_sent = defaultdict(lambda: datetime.min)
        self.ben_timeout = timedelta(seconds=30)   # 30 second cooldown
        self.socks_timeout = timedelta(seconds=30) # 30 second cooldown

    async def channel_move(self, channel: discord.channel, level, guild: discord.guild):
        if level == 1:
            new_category_id = self.config.get_archive_1_id()
        elif level == 2:
            new_category_id = self.config.get_archive_2_id()
        category = discord.utils.get(guild.categories, id=new_category_id)
        await channel.move(category=category, sync_permissions=True, beginning=True)

    async def get_channels(self, current_month, check_day, modifier=0):
        check_month = utilities.check_month(current_month - modifier)
        channels = self.archive_db.get_channels(check_month, check_day)
        if channels:
            return_channels = []
            for channel in channels:
                return_channels.append(channel[0])
            return return_channels
        return False
        
    @tasks.loop(time=time(5,0, tzinfo=timezone.utc))
    async def archive_check(self):
        current_month = datetime.now().month
        check_day = datetime.now().day
        guild = self.bot.get_guild(self.config.get_guild_id())
        three_channels = await self.get_channels(current_month, check_day, 3)
        if three_channels:
            for channel in three_channels:
                self.archive_db.update(channel, 2)
                real_channel = self.bot.get_channel(channel)
                await self.channel_move(real_channel, 2, guild)
        six_channels = await self.get_channels(current_month, check_day, 9)
        if six_channels:
            for channel in six_channels:
                real_channel = self.bot.get_channel(channel)
                self.archive_db.remove(real_channel)
                if real_channel:
                    await real_channel.delete()
                else:
                    print(channel)

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
            channel = self.bot.get_channel(self.config.get_announcements_channel_id())
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
            channel = self.bot.get_channel(self.config.get_announcements_channel_id())
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
        current_month = datetime.now().month
        current_day = datetime.now().day
        if current_month == 1 and current_day == 16:
            channel = self.bot.get_channel(self.config.get_announcements_channel_id())
            msg = self.holiday.check(1,16)
            if not msg:
                msg = "LET ME HEAR YOU SHOUT 1 1 6!\n\n Happy 116 day, everyone!"
            await channel.send(msg)

    async def handle_april_fools(self, message: discord.Message):
        star = "⭐"
        excludedChannels = [self.config.get_staff_help_id(),self.config.get_staff_id(), self.config.get_staff_bot_id(), 
                            self.config.get_report_id(), self.config.get_staff_partner_id, self.config.get_reddit_channel_id(), self.config.get_starboard_channel(),
                            902769402573881375, self.config.get_bot_commands_id, self.config.get_mod_log_id(),705478446075215893,
                            self.config.get_announcements_channel_id(), self.config.get_partners_id(), self.config.get_artist_role_menu_id(),
                            776157426113970207, self.config.get_rules_id(), self.config.get_welcome_id()] #all excluded channels for guild in question
        if message.author != self.bot.user and message.guild.id == self.config.CHH_GUILD_ID and not message.channel.id in excludedChannels:
                #odds will be 20%. 
            allowed = [3,8]
            if random.randint(1,10) in allowed:
                await message.add_reaction(star)

    async def handle_stick(self, message: discord.Message):
        allowed_ids = [489532994898362388, 806328902217760818, 613467520640221208, 806563614013915176]
        allowed_stick = ["<:stick:743597072598433924>", "<:broken_stick:769693076938817577>", 
                        "stick", "kcits", "st1ck", "st!ck", "$tick", "$t1ck", "$t!ck",
                        "5t1ck", "5t!ck", "5t1(k", "5t!k", "st1(k", "st!k",
                        "$t1(k", "$t!k", "$t1c|", "$t!c|", "$t1<k", "$t!<k",
                        "St1ck", "St!ck", "sT1ck", "sT!ck", "ST1CK", "ST!CK",
                        "$t1(k", "$t!<k", "$t1c|", "$t!c|", "$t1<|", "$t!<|",
                        "st1x", "st!x", "$t1x", "$t!x", "stix", "$tix",
                        "ѕtιcк", "ʂȶɨƈƙ", "ꜱᴛɪᴄᴋ", "₴₮ł₵₭"]
        role_ids = [role.id for role in message.author.roles]
    
        if not (message.content.lower() in allowed_stick) and not any(int(role_id) in allowed_ids for role_id in role_ids):
            await message.delete()
    
    async def handle_ben(self, message):
        now = datetime.now()
        if now - self.ben_last_sent[message.channel.id] < self.ben_timeout:
            return
        if "🥀" in message.content:
            allowed = [1,3,6,9,10]
            max_rand = 10
            if utilities.is_after("26.08.2023 22:00:00"):
                max_rand = 100
                allowed = [1, 5, 9, 13, 17, 21, 25, 29, 33, 37, 41, 45, 49, 53, 57, 61, 65, 69, 73, 77, 81, 85, 89, 93, 97]
            if utilities.is_after("01.09.2023 00:00:00"):
                max_rand = 100
                allowed = [1,3,6,9,10]
            if random.randint(1,max_rand) in allowed:
                self.ben_last_sent[message.channel.id] = now
                await message.channel.send("Yeah yeah just reply with a wilted rose")
                logger.info("Yeah yeah just reply with a wilted rose")
                

    async def handle_socks(self, message):
        now = datetime.now()
        if now - self.socks_last_sent[message.channel.id] < self.socks_timeout:
            return
        if "socks" in message.content.lower():
            max_rand = 10
            allowed = [1,2,5,7,9]
            if utilities.is_after("27.08.2023 02:00:00"):
                max_rand = 100
                allowed = [1, 5, 9, 13, 17, 21, 25, 29, 33, 37, 41, 45, 49, 53, 57, 61, 65, 69, 73, 77, 81, 85, 89, 93, 97]
            if utilities.is_after("01.09.2023 04:00:00"):
                max_rand = 100
                allowed = [1,3,6,9,10]
            if random.randint(1,max_rand) in allowed:
                self.socks_last_sent[message.channel.id] = now
                await message.channel.send("So, I don't wanna like... Knock anyone's socks off or anything, but I recently became a full time employee at a coffee shop.")
                logger.info("So, I don't wanna like... Knock anyone's socks off or anything, but I recently became a full time employee at a coffee shop.")
               
                
    @commands.Cog.listener()
    async def on_message(self, message):
        ref_msg = ""
        channel_name = message.channel.name
        if message.reference is not None:
            calling_channel = self.bot.get_channel(message.channel.id)
            ref_msg_temp = await calling_channel.fetch_message(message.reference.message_id)
            ref_msg = ref_msg_temp.content
        if self.bot.user.mentioned_in(message) and not message.author == self.bot.user:
            if not message.author.global_name == None:
                uname = message.author.global_name
            elif not message.author.nick == None:
                uname = message.author.nick
            else:
                uname = message.author.name
            async with message.channel.typing():
                response = openai.generate_answer(message.content, uname, ref_msg)
                logger.info(f"AI response generated by {uname} in {channel_name}")
                logger.info(f"Prompt: {message.content}")
                logger.info(f"Response: {response}")
                await message.reply(response)

        await self.handle_ben(message)
        await self.handle_socks(message)
        
        
        if date.today().strftime("%m/%d") == "04/01":
            await self.handle_april_fools(message)

        stick_channel = self.config.get_stick_id()
        if message.channel.id == stick_channel:
            await self.handle_stick(message)

def setup(bot):
    bot.add_cog(Events(bot))
