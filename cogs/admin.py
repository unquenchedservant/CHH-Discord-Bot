import os, discord, asyncio
from discord.ext import commands
from discord.ext.commands import has_permissions, group
from utilities import database, get_env
class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, aliases=["refresh"], usage="<admin|spotify|suggestions>")
    @has_permissions(administrator=True)
    async def reload(self, ctx, exten):
        if exten.lower() == "admin":
            self.bot.reload_extension('cogs.admin')
        elif exten.lower() == "spotify":
            self.bot.reload_extension('cogs.spotify')
        elif exten.lower() == "suggestions":
            self.bot.reload_extension('cogs.suggestions')
        await asyncio.sleep(1)
        await ctx.message.delete()

    @commands.group(invoke_without_command=True, pass_context=True, name="listeningparty", aliases=["lp", "listening", "party"], usage="<channel>")
    @has_permissions(administrator=True)
    async def listeningparty(self, ctx, *args):
        pass
    @listeningparty.command(pass_context=True, name="create", description="Create a listening party, creates a voice chat and text chat")
    @has_permissions(administrator=True)
    async def create_(self, ctx, *name):
        name = ' '.join(name)
        if len(name.split(" ")) > 1:
            await ctx.send("Please keep name to one word")
        elif name == None or name == "":
            await ctx.send("Please enter a name for the listening party")
        else:
            check = database.check_listening_party_channels(name)
            if check:
                guild = ctx.guild
                name = name.lower()
                new_cat = await guild.create_category_channel("{} LISTENING PARTY".format(name.upper()), position=0)
                text_channel = await guild.create_text_channel("{}-listening-discussion".format(name), category=new_cat)
                await text_channel.set_permissions(guild.default_role, send_messages=False)
                voice_channel = await guild.create_voice_channel("{}-listening-party".format(name), category=new_cat)
                await voice_channel.set_permissions(guild.default_role, speak=False)
                await voice_channel.set_permissions(guild.default_role, connect=False)
                voice_id = voice_channel.id
                text_id = text_channel.id
                print(text_id)
                print(voice_id)
                database.add_listening_party_channels(name, int(text_id), int(voice_id))
            else:
                await ctx.send("Listening party by that name exists already")
    @listeningparty.command(pass_context=True, name="pre", description="Pre-Listening party, voice chat allowed")
    @has_permissions(administrator=True)
    async def pre(self, ctx, name):
        print(name)
        voice_id = database.get_listening_party_voice(name)
        text_id  = database.get_listening_party_text(name)
        if voice_id == None or text_id == None:
            ctx.send("No listening party with that name")
        else:
            vc = self.bot.get_channel(voice_id)
            tc = self.bot.get_channel(text_id)
            await vc.set_permissions(ctx.guild.default_role, speak=True)
            await vc.set_permissions(ctx.guild.default_role, connect=True)
            await tc.set_permissions(ctx.guild.default_role, send_messages=True)

    @listeningparty.command(pass_context=True, name="start", description="Start at midnight, voice chat not allowed except for groovy")
    @has_permissions(administrator=True)
    async def start_(self, ctx, name):
        print(name)
        voice_id = database.get_listening_party_voice(name)
        text_id  = database.get_listening_party_text(name)
        if voice_id == None or text_id == None:
            ctx.send("No listening party with that name")
        else:
            vc = self.bot.get_channel(voice_id)
            tc = self.bot.get_channel(text_id)
            await vc.set_permissions(ctx.guild.default_role, speak=False)

    @listeningparty.command(pass_context=True, name="post", description="Open discussion back up at the end of the album")
    @has_permissions(administrator=True)
    async def post_(self, ctx, name):
        print(name)
        voice_id = database.get_listening_party_voice(name)
        text_id  = database.get_listening_party_text(name)
        if voice_id == None or text_id == None:
            ctx.send("No listening party with that name")
        else:
            vc = self.bot.get_channel(voice_id)
            tc = self.bot.get_channel(text_id)
            await vc.set_permissions(ctx.guild.default_role, speak=True)

    @listeningparty.command(pass_context=True, name="end", aliases=['delete', 'stop'], description="End the listening party, moving channel to archive and not allowing connections")
    @has_permissions(administrator=True)
    async def end_(self, ctx, name):
        print(name)
        voice_id = database.get_listening_party_voice(name)
        text_id  = database.get_listening_party_text(name)
        if voice_id == None or text_id == None:
            await ctx.send("No listening party with that name")
        else:
            vc = self.bot.get_channel(voice_id)
            tc = self.bot.get_channel(text_id)
            await tc.set_permissions(ctx.guild.default_role, send_messages=False)
            for x in ctx.guild.categories:
                if x.name == "ARCHIVED CHANNELS":
                    archive_cat = x
                if x.name == "{} LISTENING PARTY".format(name.upper()):
                    lp_cat = x
            await vc.delete()
            await tc.edit(category=archive_cat)
            await lp_cat.delete()
            database.delete_listening_party(name)

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

    @add.command(pass_context=True, name="welcome", aliases=["main", "rules"], description="Sets this channel as being the welcome channel", brief="Set a welcome channel")
    @has_permissions(administrator=True)
    async def _welcome(self, ctx):
        updated = database.set_welcome_channel(ctx.channel.id, ctx.guild.id)
        if updated:
            temp_message = await ctx.channel.send("Changed welcome channel to this channel")
        else:
            temp_message = await ctx.channel.send("Added this channel as the welcome channel")
        await asyncio.sleep(3)
        await ctx.message.delete()
        await temp_message.delete()

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

    @commands.group(invoke_without_command=True, pass_context=True, usage="welcome")
    @has_permissions(administrator=True)
    async def set(self, ctx):
        pass

    @set.command(pass_context=True, brief="Sets the welcome message")
    @has_permissions(administrator=True)
    async def welcome(self, ctx):
        initial = await ctx.channel.send("Please send the message you want to display in the welcome channel")
        def check(message):
            return message.author == ctx.message.author
        msg = await self.bot.wait_for('message', check=check)
        msg_content = msg.content
        msg_content = msg_content.replace("```", "'''")
        save_msg = "Current Welcome Raw Text:\n```\n{}\n```".format(msg_content)
        saved_msg = await ctx.channel.send(save_msg)
        await saved_msg.pin()
        channel_id = database.get_welcome_channel_id(ctx.guild.id)
        if not channel_id:
            temp = await ctx.channel.send("Please set a welcome channel")
            await asyncio.sleep(3)
            await msg.delete()
            await temp.delete()
            await initial.delete()
            await ctx.message.delete()
        else:
            welcome_channel = self.bot.get_channel(channel_id)
            msg_id = database.get_welcome_msg_id(ctx.guild.id)
            if not msg_id:
                temp = await ctx.channel.send("No welcome message found, creating it now")
                welcome_msg = await welcome_channel.send(msg.content)
                database.set_welcome_msg_id(welcome_msg.id, ctx.guild.id)
                await asyncio.sleep(3)
                await msg.delete()
                await temp.delete()
                await initial.delete()
                await ctx.message.delete()
            else:
                try:
                    original = await welcome_channel.fetch_message(msg_id)
                    await original.edit(content=msg.content)
                except:
                    new_msg = await welcome_channel.send(msg.content)
                    database.set_welcome_msg_id(new_msg.id, ctx.guild.id)
                temp = await ctx.channel.send("Updated welcome message")
                await asyncio.sleep(3)
                await msg.delete()
                await temp.delete()
                await initial.delete()
                await ctx.message.delete()


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
