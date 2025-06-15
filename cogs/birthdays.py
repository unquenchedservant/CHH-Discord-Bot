import discord
from discord.commands import (slash_command)
from discord.commands import Option
from discord import option
from discord.ext import commands
from discord import SlashCommandGroup
from utilities.database import Birthday
import utilities
from datetime import time, timezone, datetime
from discord.ext import tasks
from utilities.logging import logger

class Birthdays(commands.Cog):
    birthdaygrp = SlashCommandGroup(name="birthday", description="CHH Birthday commands")

    def __init__(self, bot):
        self.bot = bot
        self.birthday = Birthday()

    @birthdaygrp.command( description="Set your birthday on the server to get a shout-out!")    
    async def set(
        self, 
        ctx: discord.ApplicationContext, 
        month: Option(int, "Enter your birth month", min_value=1, max_value=12, required=True),  # type: ignore
        day: Option(int, "Enter your birth date", min_value=1, max_value=31, required=True) # type: ignore
    ):
        logger.info("setbirthday - User: {}".format(ctx.author.name))
        if not month:
            await ctx.respond("Please enter your birth month (1-12)")
        elif not day:
            await ctx.respond("Please enter your birth date (1-31)")
        else:
            self.birthday.set(ctx.author.id, month, day) 
            await ctx.respond("Your birthday has been set successfully", ephemeral=True)

    @birthdaygrp.command( description="Check to make sure you have your birthday set correctly")
    async def check(self, ctx: discord.ApplicationContext):
        logger.info("check birthday - User: {}".format(ctx.author.name))
        birthday = self.birthday.get(ctx.author.id)
        if birthday == [0, 0]:
            await ctx.respond("You do not have a birthday set, use `/setbirthday` to do so", ephemeral=True)
        else:
            await ctx.respond("Your birthday is set to {}/{}".format(birthday[0], birthday[1]), ephemeral=True)

    @birthdaygrp.command( description="Removes you from our birthday list")
    async def remove(self, ctx: discord.ApplicationContext):
        logger.info("remove birthday - User: {}".format(ctx.author.name))
        self.birthday.remove(ctx.author.id)
        await ctx.respond("Your birthday has been removed successfully", ephemeral=True)
        
def setup(bot):
    bot.add_cog(Birthdays(bot))