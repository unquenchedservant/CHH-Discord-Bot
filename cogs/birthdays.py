import discord
from discord.commands import (slash_command)
from discord.commands import Option
from discord.ext import commands
from utilities import database
import utilities

ERROR_MSG = "You need to be a mod or admin to use this command"

GUILD_ID=utilities.get_guild_ids(False)

class Birthdays(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    

def setup(bot):
    bot.add_cog(Birthdays(bot))