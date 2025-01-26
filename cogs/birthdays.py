import discord
from discord.commands import (slash_command)
from discord.commands import Option
from discord import option
from discord.ext import commands
from utilities import database
import utilities
from datetime import time, timezone, datetime
from discord.ext import tasks

GUILD_ID=utilities.get_guild_ids(utilities.get_is_dev())

class Birthdays(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
        
def setup(bot):
    bot.add_cog(Birthdays(bot))