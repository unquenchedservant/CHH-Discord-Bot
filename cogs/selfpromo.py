from ctypes import util
from time import sleep

import discord
from utilities import Config
from discord.commands import Option, message_command, slash_command
from discord.ext import commands
from utilities.database import SelfPromoMsg
from utilities.logging import logger

class SelfPromo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config()
        self.selfpromomsg = SelfPromoMsg()

    async def check_validity(self, ctx: discord.ApplicationContext, user:discord.Member, type: str):
        logger.info("Self-Promo report ({}) - Reporter: {} | Reportee: {}".format(type, ctx.author.name, user.name))
        try:
            if user.roles:
                pass
        except AttributeError:
            logger.info("Self-Promo report ({}) - Automated Message | No Action".format(type))
            await ctx.respond(
                "This appears to be an automated message, thanks though! (Please reach out to Chill if you think this was an error)",
                ephemeral=True,
            )
            return False
        user_roles = [y.name.lower() for y in user.roles]
        if "verified artist" in user.roles:
            logger.info("Self-Promo report ({}) - Verified Artist | No Action".format(type))
            await ctx.respond(
                "Thank you for the report, but this is a verified artist",
                ephemeral=True,
            )
            return False
        elif "mod" in user_roles:
            logger.info("Self-Promo report ({}) - Mod | No Action".format(type))
            await ctx.respond(
                "Thank you for the report, but this is a mod.", ephemeral=True
            )
            return False
        elif "admin" in user_roles:
            logger.info("Self-Promo report ({}) - Admin | No Action".format(type))
            await ctx.respond(
                "Thank you for the report, but this is an admin.",
                ephemeral=True,
            )
            return False
        elif user.bot:
            if user.id==701044392378499152:
                logger.info("Self-Promo report ({}) - CHH Bot | Put on blast".format(type))
                await ctx.respond("You thought.", ephemeral=False)
            else:
                logger.info("Self-Promo report ({}) - Bot | No Action".format(type))
                await ctx.respond("Thank you, but this is a bot", ephemeral=True)
            return False
        return True

    @message_command(name="Mark Self-Promo")
    async def selfpromo(self, ctx, message: discord.Message):
        user = message.author
        if self.selfpromomsg.check(message.id):
            await ctx.respond(
                "This message has already been reported, thank you!", ephemeral=True
            )
        else:
            if user:                
                msg = "Woah there, <@{}>,".format(user.id)
                valid = await self.check_validity(ctx, user, "App")
                if not valid:
                    return 0
            else:
                logger.info("Self-Promo report (App) - Reporter: {} | Reportee: N/A (HOW DID YOU DO THIS?!)".format(ctx.author.name))
                msg = "Woah there,"
            msg = msg + " it looks like you're sharing self-promotion outside of <#{}>!\n\n".format(self.config.get_self_promo_id())
            msg = msg + "If you don't have access to that channel, please stick around and get to know us a bit. Shortly after you join you will gain access. \n\n"
            msg = msg + "In the meantime, check out <#{}> and assign yourself the Artist/Producer tag to unlock some extra channels. Please take a minute to check out our <#{}>\n\n".format(self.config.get_role_menu_id(), self.config.get_rules_id())
            msg = msg + "If you feel you should be a verified artist (who can self promo anywhere) feel free to reach out to the mods. Requirements: 50,000 streams on a single song *or* 10,000 monthly streams.\n\n"
            msg = msg + "If we don't know who you are, we likely won't care about your music."
            
            embed = discord.Embed(title="Please don't self promo", description=msg)
            # embed.set_image(url="https://i.imgur.com/MQMdhiE.jpeg")
            await ctx.send(embed=embed)
            await ctx.respond(
                "Thanks, we let the user know about our self promotion rule!",
                ephemeral=True,
            )
            self.selfpromomsg.add(message.id)
            report_channel = self.bot.get_channel(self.config.get_report_id())
            report_msg = "The following message was tagged for self-promotion by <@{}>:\n{}\n".format(ctx.author.id, message.jump_url)
            
            await report_channel.send(report_msg)

    @slash_command(
        
        default_permissions=True,
        description="Use this when someone posts self promotion, or if someone asks about self promotion",
    )
    async def selfpromoalert(
        self,
        ctx: discord.ApplicationContext,
        user: Option(
            discord.Member, "optional: Tag the user", required=False, default=None
        ), # type: ignore
    ):
        if user:
            valid = await self.check_validity(ctx, user, "slash")
            if not valid:
                return 0
            logger.info("Self-Promo report ({}) - Reporter: {} | Reportee: {}".format("slash", ctx.author.name, user.name))
            title_str = "Please don't self-promote"
            msg = "Woah there, <@{}?," + str(user.id) + ">,"
            msg = msg + " it looks like you're sharing self-promotion outside of <#{}>!\n\n".format(self.config.get_self_promo_id())
            report_msg = "<@{}> was tagged for self-promotion by <@{}>. \n\nJump to message:{}\n".format(user.id, ctx.author.id, embed_msg.jump_url)
            report_channel = self.bot.get_channel(self.config.get_report_id())
            sleep(5)
            await report_channel.send(report_msg)
            
        else:
            logger.info("Self-Promo report ({}) - Reporter: {} | Reportee: N/A".format("slash", ctx.author.name))
            title_str = "A Reminder About Our Self Promotion Rule"
            msg = "Please only self-promote in <#{}>!\n\n".format(self.config.get_self_promo_id())
        msg = msg + "If you don't have access to that channel, please stick around and get to know us a bit. Shortly after you join you will gain access. \n\n"
        msg = msg + "In the meantime, check out <#{}> and assign yourself the Artist/Producer tag to unlock some extra channels. Also, please take a minute to check out our <#{}>\n\n".format(self.config.get_role_menu_id(), self.config.get_rules_id())
        msg = msg + "If you feel you should be a verified artist (who can self promote anywhere) feel free to reach out to the mods. Requirements:\n50,000 streams on a single song *OR*\n10,000 monthly streams.\n\n"
        msg = msg + "If we don't know who you are, we likely won't care about your music."
            
        embed = discord.Embed(title=title_str, description=msg)    
        await ctx.send(embed=embed)
        await ctx.respond("Thanks, we let the user/channel know about our self promotion rule!", ephemeral=True)

def setup(bot):
    bot.add_cog(SelfPromo(bot))
