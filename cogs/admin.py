import os, discord, asyncio
from discord.ext import commands
from discord.ext.commands import has_permissions, group
from utilities import database, get_env
class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """
    Track/Add/Start Command Group

    Subcommands:
        suggestions
        recommendations
    """
    @commands.group(invoke_without_command=True, pass_context=True, aliases=["start"], usage="<suggestion|recommendations>", brief="Add a tracked channel", description="Start listening to a channel for suggestions or recommendations")
    @has_permissions(administrator=True)
    async def add(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title="Error Adding Tracking", description="Please specify one of the following", colour=0x0099ff)
            embed.set_author(name="r/CHH Bot", icon_url="https://i.imgur.com/ZNdCFKg.png")
            embed.add_field(name="suggestions", value="tracks a suggestion channel")
            embed.add_field(name="\u200b", value="\u200B")
            embed.add_field(name="\u200b", value="\u200B")
            embed.add_field(name="recommendations", value="tracks a recommendation channel")
            await ctx.channel.send(embed=embed)

    @add.command(pass_context=True, aliases=["suggest", "sug", "suggestion", "s"],name="suggestions", description="Start listening to this channel for suggestions")
    @has_permissions(administrator=True)
    async def _suggestions(self, ctx):
        success = database.add_suggestion_channel(ctx.channel.id)
        if success:
            temp_message = await ctx.channel.send("Started listening to this channel for suggestions")
        else:
            temp_message = await ctx.channel.send("Already listening to this channel for suggestions")
        await asyncio.sleep(3)
        await ctx.message.delete()
        await temp_message.delete()

    @add.command(aliases=["recommendation", "recommend", "rec", "r"],name="recommendations", description="Start listening to this channel for recommendations")
    @has_permissions(administrator=True)
    async def _recommendations(self, ctx):
        success = database.add_recommendation_channel(ctx.channel.id)
        if success:
            temp_message = await ctx.channel.send("Started listening to this channel for recommendations")
        else:
            temp_message = await ctx.channel.send("Already listening to this channel for recommendations")
        await asyncio.sleep(3)
        await ctx.message.delete()
        await temp_message.delete()

    """
    Remove/Disable/Untrack/Stop Command Group

    Subcommands:
    - suggestions
    - recommendations
    """
    @group(case_insensitive=True, aliases=["disable", "untrack", "stop"], usage="<suggestions|recommendations>", brief="Remove a tracked channel", description="Stops listening for suggestions/recommendations on a channel")
    @has_permissions(administrator=True)
    async def remove(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title="Error Stopping Listening", description="Please specify one of the following", colour=0x0099ff)
            embed.set_author(name="r/CHH Bot", icon_url="https://i.imgur.com/ZNdCFKg.png")
            embed.add_field(name="suggestions", value="Stop listening for suggestions on the channel")
            embed.add_field(name="\u200b", value="\u200B")
            embed.add_field(name="\u200b", value="\u200B")
            embed.add_field(name="recommendations", value="Stop listening for recommendations on the channel")
            await ctx.channel.send(embed=embed)

    @remove.command(aliases=["suggest", "sug", "suggestion", "s"], description="Stop listening to this channel for suggestions")
    async def suggestions(self, ctx):
        success = database.remove_suggestion_channel(ctx.channel.id)
        if success:
            temp_message = await ctx.channel.send("No longer listening to this channel for suggestions")
        else:
            temp_message = await ctx.channel.send("Was not listening this channel for suggestions")
        await asyncio.sleep(3)
        await ctx.message.delete()
        await temp_message.delete()

    @remove.command(aliases=["recommendation", "recommend", "rec", "r"], description="Stop listening to this channel for recommendations")
    async def recommendations(self, ctx):
        success = database.remove_recommendation_channel(ctx.channel.id)
        if success:
            temp_message = await ctx.channel.send("No longer listening to this channel for recommendations")
        else:
            temp_message = await ctx.channel.send("Was not listening this channel for recommendations")
        await asyncio.sleep(3)
        await ctx.message.delete()
        await temp_message.delete()

    """
    Other Commands

    Shutdown - Owner only, shuts the bot down remotely
    Clear - AKA purge, clears X messages from the channel
    Prefix - set the prefix for the server
    """
    @commands.command(hidden=True)
    async def shutdown(self, ctx):
        if ctx.message.author.id == int(get_env.owner_id()):
            try:
                await ctx.channel.send("Shutting Down")
                await self.bot.logout()
            except:
                print("EnvironmentError")
                self.bot.clear()
        else:
            await ctx.channel.send("Hey wait a second, you aren't my owner")

    @commands.command(aliases=["purge"], usage="<number of messages to purge>", brief="clear X amount of messages in channel", description="Clear the previous X messages on this channel")
    @has_permissions(administrator=True)
    async def clear(self, ctx, amount: int):
        msgs = []
        await ctx.channel.purge(limit=amount+1)

    @commands.command(aliases=["set_prefix"], usage="<wanted_prefix>", brief="Change the prefix for the server", description="Set a max 2-character prefix for this bot on this server")
    @has_permissions(administrator=True)
    async def prefix(self, ctx, new_prefix=""):
        if new_prefix == "":
            embed = discord.Embed(title="Prefix", description="Get or change the server prefix", colour=0x0099ff)
            embed.set_author(name="r/CHH Bot", icon_url="https://i.imgur.com/ZNdCFKg.png")
            embed.add_field(name="Current prefix", value="{}".format(database.get_prefix(ctx.guild.id)))
            embed.add_field(name="\u200B", value="\u200B")
            embed.add_field(name="\u200B", value="\u200B")
            embed.add_field(name="Change Prefix", value="To change the prefix, use {}prefix <new prefix>".format(database.get_prefix(ctx.guild.id)), inline=True)
            await ctx.channel.send(embed=embed)
        else:
            if len(new_prefix) > 2:
                embed = discord.Embed(title="Invalid Prefix", description="Please make sure that your prefix is at max two characters", colour=0x0099ff)
                embed.set_author(name="r/CHH Bot", icon_url="https://i.imgur.com/ZNdCFKg.png")
                embed.add_field(name="Change Prefix", value="To change the prefix, use {}prefix <new prefix>".format(database.get_prefix(ctx.guild.id)), inline=True)
                await ctx.channel.send(embed=embed)
            else:
                database.set_prefix(ctx.guild.id, new_prefix)
                await ctx.channel.send("Successfully updated prefix for server")

def setup(bot):
    bot.add_cog(Admin(bot))
