from ctypes import util

import discord
import utilities
from discord.commands import Option, slash_command, message_command
from discord.ext import commands
from utilities import database

GUILD_ID = utilities.get_guild_ids()
SELF_PROMO_CHANNEL = utilities.get_self_promo_id()
ROLE_MENU_CHANNEL = utilities.get_role_menu_id()
RULE_CHANNEL = utilities.get_rules_id()

class SelfPromo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @message_command(name="Mark Self-Promo")
    async def selfpromo(self,ctx, message: discord.Message):
        user = message.author
        if user:
            msg = "Woah there, <@" + str(user.id) + ">,"
        else:
            msg = "Woah there,"
        msg = msg + " it looks like you're sharing self-promotion outside of <#" + str(SELF_PROMO_CHANNEL) + ">!\n\n"
        msg = msg + "If you don't have access to that channel, please stick around and get to know us a bit. Shortly after you join you will gain access. \n\n"
        msg = msg + "In the meantime, check out <#" + str(ROLE_MENU_CHANNEL) + "> and assign yourself the Artist/Producer tag to unlock some extra channels. Please take a minute to check out our <#" + str(RULE_CHANNEL) + ">\n\n"
        msg = msg + "If we don't know who you are, we likely won't care about your music."
        embed = discord.Embed(title="Please don't self promo", description=msg)
        #embed.set_image(url="https://i.imgur.com/MQMdhiE.jpeg")
        await ctx.send(embed=embed)
        await ctx.respond("Thanks, we let the user know about our self promotion rule!", ephemeral=True)
    @slash_command(
        guild_ids=GUILD_ID,
        default_permissions=True,
        description="Use this when someone posts self promotion",
    )
    async def selfpromoalert(self, ctx: discord.ApplicationContext, user: Option(discord.Member, "optional: Tag the user", required=False, default=None)):
        if user:
            msg = "Woah there, <@" + str(user.id) + ">,"
        else:
            msg = "Woah there,"
        msg = msg + " it looks like you're sharing self-promotion outside of <#" + str(SELF_PROMO_CHANNEL) + ">!\n\n"
        msg = msg + "If you don't have access to that channel, please stick around and get to know us a bit. Shortly after you join you will gain access. \n\n"
        msg = msg + "In the meantime, check out <#" + str(ROLE_MENU_CHANNEL) + "> and assign yourself the Artist/Producer tag to unlock some extra channels. Please take a minute to check out our <#" + str(RULE_CHANNEL) + ">\n\n"
        msg = msg + "If we don't know who you are, we likely won't care about your music."
        embed = discord.Embed(title="Please don't self promo", description=msg)
        #embed.set_image(url="https://i.imgur.com/MQMdhiE.jpeg")
        await ctx.send(embed=embed)
        await ctx.respond("Thanks, we let the user know about our self promotion rule!", ephemeral=True)


def setup(bot):
    bot.add_cog(SelfPromo(bot))
