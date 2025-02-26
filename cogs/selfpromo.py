from ctypes import util
from time import sleep

import discord
import utilities
from discord.commands import Option, message_command, slash_command
from discord.ext import commands
from utilities import database

GUILD_ID = utilities.get_guild_ids()
SELF_PROMO_CHANNEL = utilities.get_self_promo_id()
ROLE_MENU_CHANNEL = utilities.get_role_menu_id()
RULE_CHANNEL = utilities.get_rules_id()
ADMIN_CHANNEL = utilities.get_admin_id()


class SelfPromo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @message_command(name="Mark Self-Promo", guild_ids=GUILD_ID)
    async def selfpromo(self, ctx, message: discord.Message):
        user = message.author
        if database.checkSelfPromoMsg(message.id):
            await ctx.respond(
                "This message has already been reported, thank you!", ephemeral=True
            )
        else:
            if user:
                print("[CHH BOT] Self-Promo report (App) - Reporter: {} | Reportee: {}".format(ctx.author.name, user.name))
                msg = "Woah there, <@" + str(user.id) + ">,"
                try:
                    print(user.roles)
                except AttributeError:
                    print("[CHH BOT] Self-Promo report (App) - Automated Message | No Action")
                    await ctx.respond(
                        "This appears to be an automated message, thanks though! (Please reach out to Chill if you think this was an error)",
                        ephemeral=True,
                    )
                    return 0
                if "verified artist" in [y.name.lower() for y in user.roles]:
                    print("[CHH BOT] Self-Promo report (App) - Verified Artist | No Action")
                    await ctx.respond(
                        "Thank you for the report, but this is a verified artist",
                        ephemeral=True,
                    )
                    return 0
                if "mod" in [y.name.lower() for y in user.roles]:
                    print("[CHH BOT] Self-Promo report (App) - Mod | No Action")
                    await ctx.respond(
                        "Thank you for the report, but this is a mod.", ephemeral=True
                    )
                    return 0
                if "admin" in [y.name.lower() for y in user.roles]:
                    print("[CHH BOT] Self-Promo report (App) - Admin | No Action")
                    await ctx.respond(
                        "Thank you for the report, but this is an admin.",
                        ephemeral=True,
                    )
                    return 0
                if user.bot:
                    if user.id==701044392378499152:
                        print("[CHH BOT] Self-Promo report (App) - CHH Bot | Put on blast")
                        await ctx.respond("You thought.", ephemeral=False)
                    else:
                        print("[CHH BOT] Self-Promo report (App) - Bot | No Action")
                        await ctx.respond("Thank you, but this is a bot", ephemeral=True)
                    return 0
            else:
                print("[CHH BOT] Self-Promo report (App) - Reporter: {} | Reportee: N/A (HOW DID YOU DO THIS?!)".format(ctx.author.name))
                msg = "Woah there,"
            msg = (
                msg
                + " it looks like you're sharing self-promotion outside of <#"
                + str(SELF_PROMO_CHANNEL)
                + ">!\n\n"
            )
            msg = (
                msg
                + "If you don't have access to that channel, please stick around and get to know us a bit. Shortly after you join you will gain access. \n\n"
            )
            msg = (
                msg
                + "In the meantime, check out <#"
                + str(ROLE_MENU_CHANNEL)
                + "> and assign yourself the Artist/Producer tag to unlock some extra channels. Please take a minute to check out our <#"
                + str(RULE_CHANNEL)
                + ">\n\n"
            )
            msg = (
                msg
                + "If you feel you should be a verified artist (who can self promo anywhere) feel free to reach out to the mods. Requirements: 50,000 streams on a single song *or* 10,000 monthly streams.\n\n"
            )
            msg = (
                msg
                + "If we don't know who you are, we likely won't care about your music."
            )
            embed = discord.Embed(title="Please don't self promo", description=msg)
            # embed.set_image(url="https://i.imgur.com/MQMdhiE.jpeg")
            await ctx.send(embed=embed)
            await ctx.respond(
                "Thanks, we let the user know about our self promotion rule!",
                ephemeral=True,
            )
            database.addSelfPromoMsg(message.id)
            report_channel = self.bot.get_channel(ADMIN_CHANNEL)
            report_msg = (
                "The following message was tagged for self-promotion by <@"
                + str(ctx.author.id)
                + ">:\n"
                + message.jump_url
                + "\n"
            )
            await report_channel.send(report_msg)

    @slash_command(
        guild_ids=GUILD_ID,
        default_permissions=True,
        description="Use this when someone posts self promotion, or if someone asks about self promotion",
    )
    async def selfpromoalert(
        self,
        ctx: discord.ApplicationContext,
        user: Option(
            discord.Member, "optional: Tag the user", required=False, default=None
        ),
    ):
        if user:
            print("[CHH BOT] Self-Promo report (slash) - Reporter: {} | Reportee: {}".format(ctx.author.name, user.name))
            msg = "Woah there, <@" + str(user.id) + ">,"
            if "verified artist" in [y.name.lower() for y in user.roles]:
                print("[CHH BOT] Self-Promo report (slash) - Verified Artist | No Action")
                await ctx.respond(
                    "Thank you for the report, but this is a verified artist",
                    ephemeral=True,
                )
                return 0
            if "mod" in [y.name.lower() for y in user.roles]:
                print("[CHH BOT] Self-Promo report (slash) - Mod | No Action")
                await ctx.respond(
                    "Thank you for the report, but this is a mod.", ephemeral=True
                )
                return 0
            if "admin" in [y.name.lower() for y in user.roles]:
                print("[CHH BOT] Self-Promo report (slash) - Admin | No Action")
                await ctx.respond(
                    "Thank you for the report, but this is an admin.", ephemeral=True
                )
                return 0
            if user.bot:
                if user.id == 701044392378499152:
                    print("[CHH BOT] Self-Promo report (slash) - CHH BOT | Put on Blast")
                    await ctx.respond("You thought.", ephemeral=False)
                else:
                    print("[CHH BOT] Self-Promo report (slash) - Verified Bot | No Action")
                    await ctx.respond("Thank you, but this is a bot", ephemeral=True)
                return 0
            msg = (
                msg
                + "it looks like you're sharing self-promotion outside of <#"
                + str(SELF_PROMO_CHANNEL)
                + ">!\n\n"
            )
            msg = (
                msg
                + "If you don't have access to that channel, please stick around and get to know us a bit. Shortly after you join you will gain access. \n\n"
            )
            msg = (
                msg
                + "In the meantime, check out <#"
                + str(ROLE_MENU_CHANNEL)
                + "> and assign yourself the Artist/Producer tag to unlock some extra channels. Also, please take a minute to check out our <#"
                + str(RULE_CHANNEL)
                + ">\n\n"
            )
            msg = (
                msg
                + "If you feel you should be a verified artist (who can self promote anywhere) feel free to reach out to the mods. Requirements:\n50,000 streams on a single song *OR*\n10,000 monthly streams.\n\n"
            )
            msg = (
                msg
                + "If we don't know who you are, we likely won't care about your music."
            )
            embed = discord.Embed(title="Please don't self promote", description=msg)
            embed_msg = await ctx.send(embed=embed)
            await ctx.respond(
                "Thanks, we let the user know about our self promotion rule!"
            )
            report_channel = self.bot.get_channel(ADMIN_CHANNEL)
            sleep(5)
            report_msg = (
                "<@"
                + str(user.id)
                + "> was tagged for self-promotion by <@"
                + str(ctx.author.id)
                + ">. \n\nJump to message: "
                + embed_msg.jump_url
                + "\n"
            )
            await report_channel.send(report_msg)
        else:
            print("[CHH BOT] Self-Promo report (slash) - Reporter: {} | Reportee: N/A".format(ctx.author.name))
            msg = (
                "Please only self-promote in <#"
                + str(SELF_PROMO_CHANNEL)
                + ">!\n\n"
            )
            msg = (
                msg
                + "If you don't have access to that channel, please stick around and get to know us a bit. Shortly after you join you will gain access. \n\n"
            )
            msg = (
                msg
                + "In the meantime, check out <#"
                + str(ROLE_MENU_CHANNEL)
                + "> and assign yourself the Artist/Producer tag to unlock some extra channels. Please take a minute to check out our <#"
                + str(RULE_CHANNEL)
                + ">\n\n"
            )
            msg = (
                msg
                + "If you feel you should be a verified artist (who can self promo anywhere) feel free to reach out to the mods. Requirements: 50,000 streams on a single song *or* 10,000 monthly streams.\n\n"
            )
            msg = (
                msg
                + "If we don't know who you are, we likely won't care about your music."
            )
            embed = discord.Embed(title="A Reminder About Our Self Promotion Rule", description=msg)
            # embed.set_image(url="https://i.imgur.com/MQMdhiE.jpeg")
            await ctx.send(embed=embed)
            await ctx.respond(
                "Thanks, we reminded the channel about our self promotion rule!",
                ephemeral=True,
            )


def setup(bot):
    bot.add_cog(SelfPromo(bot))
