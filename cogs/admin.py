import os
import discord
import asyncio
from discord.ext import commands
from discord.ext.commands import has_permissions, group
from utilities import database

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True, aliases=["setreport","addreport", "updatereport"])
    @has_permissions(administrator=True)
    async def setreportchannel(self, ctx):
        guild = ctx.guild
        channel = ctx.channel
        if database.lookUpGuildReport(guild.id):
            database.updateGuildReport(guild.id, channel.id)
            await ctx.send("Updated the report channel for this server")
        else:
            database.setGuildReport(guild.id, channel.id)
            await ctx.send("Added a report channel for this server")
    @commands.command(pass_context=True, name="removereportchannel", aliases=["removeReport"])
    @has_permissions(administrator=True)
    async def removereportchannel(self, ctx):
        guild = ctx.guild
        if database.lookUpGuildReport(guild.id):
            database.removeGuildReport(guild.id)
            await ctx.send("Removed the report channel for this server")

    @commands.command(pass_context=True)
    @has_permissions(administrator=True)
    async def toggleRoleMemory(self, ctx):
        database.toggleRoleMemory(ctx.guild.id)
def setup(bot):
    bot.add_cog(Admin(bot))