from discord.ext import commands
from datetime import date
import random
import utilities

class AprilFools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        star = "⭐"
        excludedChannels = [utilities.STAFF_HELP_CHANNEL_ID, utilities.STAFF_CHANNEL_ID, utilities.STAFF_BOT_CHANNEL_ID, 
        utilities.REPORT_CHANNEL_ID, utilities.STAFF_PARTNER_CHANNEL_ID, utilities.REDDIT_CHANNEL_ID, utilities.STARBOARD_ID, 
        902769402573881375, utilities.BOT_COMMANDS_CHANNEL_ID, utilities.MOD_LOG_CHANNEL_ID, 705478446075215893, 
        utilities.ANNOUNCEMENTS_CHANNEL_ID, utilities.PARTNERS_CHANNEL_ID, utilities.ARTIST_ROLE_MENU_CHANNEL_ID, 776157426113970207, 
        utilities.RULE_CHANNEL_ID, utilities.WELCOME_CHANNEL_ID] #all excluded channels for guild in question
        if message.author != self.bot.user and message.guild.id == utilities.CHH_GUILD_ID:
            if self.aprilFools(message) and not message.channel.id in excludedChannels:
                #odds will be 20%. 
                allowed = [3,8]
                if random.randint(1,10) in allowed:
                    await message.add_reaction(star)
                    
    def aprilFools(self, message):
        if date.today().strftime("%m/%d") == "04/01": #april fools day
            return True
        else:
            return False

def setup(bot):
    bot.add_cog(AprilFools(bot))
