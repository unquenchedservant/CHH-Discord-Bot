from discord.ext import commands
from datetime import date
import random 

class AprilFools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        star = "⭐"
        excludedChannels = [909151861892866158,705463143882686564,685566940122447887, 705532389744705616, 832352549164154900, 700486332979609671, 786775284484669460, 902769402573881375, 702927203360571483, 705478973651419167, 705478446075215893, 613469111682334762, 797240025653051402, 616100468526940195, 776157426113970207, 844989137551228978, 613468039010320415] #all excluded channels for guild in question
        if message.author != self.bot.user and message.guild.id == 613464665661636648:
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