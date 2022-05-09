import discord
from discord.commands import (slash_command)
from discord.commands import Option
from discord.ext import commands
from utilities import database

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    
    @slash_command(guild_ids=[365879579887534080], default_permission=False)
    @commands.has_any_role("ADMIN", "MOD")
    async def setreportchannel(self, ctx: discord.ApplicationContext, channel: Option(discord.TextChannel, "Channel", required=True)):
        try:
            guild = ctx.guild
            if database.lookUpGuildReport(guild.id):
                database.updateGuildReport(guild.id, channel.id)
                await ctx.respond("Updated the report channel for this server", ephemeral=True)
            else:
                database.setGuildReport(guild.id, channel.id)
                await ctx.respond("Added a report channel for this server", ephemeral=True)
        except discord.ext.commands.errors.MissingAnyRole:
            await ctx.respond("Something went wrong, are you a mod or admin?")

    @slash_command(guild_ids=[365879579887534080], default_permission=False)
    @commands.has_any_role("ADMIN", "MOD")
    async def removereportchannel(self, ctx: discord.ApplicationContext):
        guild = ctx.guild
        if database.lookUpGuildReport(guild.id):
            database.removeGuildReport(guild.id)
            await ctx.respond("Removed the report channel for this server", ephemeral=True)

    @slash_command(guild_ids=[365879579887534080], default_permission=False)
    @commands.has_any_role("ADMIN", "MOD")
    async def togglerolememory(self, ctx: discord.ApplicationContext):
        status = database.checkRoleMemory(ctx.guild.id)
        msg = ""
        if status == 1:
            msg = "Role memory has been turned off for this server"
        if status == 0:
            msg = "Role memory has been turned on for this server"
        database.toggleRoleMemory(ctx.guild.id)
        await ctx.respond(msg, ephemeral=True)
    
    @slash_command(guild_ids=[365879579887534080], default_permission=False)
    @commands.has_any_role("ADMIN", "MOD")
    async def checkrolememory(self, ctx: discord.ApplicationContext):
        status = database.checkRoleMemory(ctx.guild.id)
        msg = ""
        if status == 1:
            msg = "Role memory is turned on on this server"
        else:
            msg = "Role memory is turned off on this server"
        await ctx.respond(msg, ephemeral=True)
def setup(bot):
    bot.add_cog(Admin(bot))