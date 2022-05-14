import discord
from discord.commands import (slash_command)
from discord.commands import Option
from discord.ext import commands
from utilities import database

ERROR_MSG = "You need to be a mod or admin to use this command"
class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    
    @slash_command(default_permission=False)
    async def togglerolememory(self, ctx: discord.ApplicationContext):
        if ctx.author.guild_permissions.administrator:
            status = database.checkRoleMemory(ctx.guild.id)
            msg = ""
            if status == 1:
                msg = "Role memory has been turned off for this server"
            if status == 0:
                msg = "Role memory has been turned on for this server"
            database.toggleRoleMemory(ctx.guild.id)
            await ctx.respond(msg, ephemeral=True)
        else:
            await ctx.respond(ERROR_MSG, ephemeral=True)
    
    @slash_command(default_permission=False)
    async def checkrolememory(self, ctx: discord.ApplicationContext):
        if ctx.author.guild_permissions.administrator:
            status = database.checkRoleMemory(ctx.guild.id)
            msg = ""
            if status == 1:
                msg = "Role memory is turned on on this server"
            else:
                msg = "Role memory is turned off on this server"
            await ctx.respond(msg, ephemeral=True)
        else:
            await ctx.respond(ERROR_MSG, ephemeral=True)
def setup(bot):
    bot.add_cog(Admin(bot))