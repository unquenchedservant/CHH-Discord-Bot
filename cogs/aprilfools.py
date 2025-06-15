from discord.ext import commands
from datetime import date
import random
import utilities
from utilities import Config

class AprilFools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config()

    @commands.Cog.listener()
    async def on_message(self, message):
        star = "⭐"
        excludedChannels = [self.config.get_staff_help_id(),self.config.get_staff_id(), self.config.get_staff_bot_id(), 
                            self.config.get_report_id(), self.config.get_staff_partner_id, self.config.get_reddit_channel_id(), self.config.get_starboard_channel(),
                            902769402573881375, self.config.get_bot_commands_id, self.config.get_mod_log_id(),705478446075215893,
                            self.config.get_announcements_channel_id(), self.config.get_partners_id(), self.config.get_artist_role_menu_id(),
                            776157426113970207, self.config.get_rules_id(), self.config.get_welcome_id()] #all excluded channels for guild in question
        if message.author != self.bot.user and message.guild.id == self.config.CHH_GUILD_ID:
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
