import discord, os
from discord.ext import commands
from discord.utils import get
from utilities import database

class Suggestions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def check_is_mod(user):
        is_mod = False
        for r in user.roles:
            for p in r.permissions:
                if p[0] == "administrator" and p[1] == True:
                    is_mod = True
        return is_mod

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        yes = "💯"
        no = "🚫"
        user = get(self.bot.get_all_members(), id=payload.user_id)
        if not payload.user_id == self.bot.user.id:
            channel = get(self.bot.get_all_channels(), id=payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            if payload.channel_id in database.get_suggestion_channels() and payload.member.guild_permissions.administrator:
                if payload.emoji.name == no:
                    await message.clear_reactions()
                    await message.add_reaction(no)
                    await channel.send("Sorry {}, your suggestion has been denied. {} will tell you why.".format(message.author.mention, user.mention))
                elif payload.emoji.name == yes:
                    await message.clear_reactions()
                    await message.add_reaction(yes)
                    await channel.send("Good news, {}, your suggestion has been accepted".format(message.author.mention))

    @commands.Cog.listener()
    async def on_message(self, message):
        yes = "✅"
        no = "❌"
        if not message.author.id == self.bot.user.id:
            suggestion_prefixes = ["[SUBREDDIT]","[DISCORD]","[CHH_BOT]","[CHH]"]
            is_mod = message.author.guild_permissions.administrator
            was_suggestion = False
            if message.channel.id in database.get_suggestion_channels() and not message.content.startswith(database.get_prefix(message.guild.id)):
                valid_msg = False
                content = message.content
                content = content.upper()
                for pfx in suggestion_prefixes:
                    if content.startswith(pfx):
                        await message.add_reaction(yes)
                        await message.add_reaction(no)
                        valid_msg = True
                if not valid_msg and not is_mod:
                    temp_message = await message.channel.send("%s please use [SUBREDDIT], [DISCORD], [CHH_BOT] or [CHH] before your suggestion" % message.author.mention)
                    await asyncio.sleep(3)
                    await message.delete()
                    await temp_message.delete()


def setup(bot):
    bot.add_cog(Suggestions(bot))
