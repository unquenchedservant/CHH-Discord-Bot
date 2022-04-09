import discord 
import time
from discord.ext import commands
from utilities import database

class Reports(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, name="report")
    async def report(self, ctx, *args):
        await ctx.message.delete()
        no_report_msg = "```\n!report <report_message>\n        ^^^^^^^^^^^^^^^^\nreport_message is a required argument that is missing.```"
        no_channel_msg = "```\nNo report channel exists on this server. \n\nPlease notify an admin or mod immediately```"
        if len(args) == 0:
            await ctx.send(no_report_msg)
            
        elif not database.lookUpGuildReport(ctx.guild.id):
            await ctx.send(no_channel_msg)
        else:
            msgContent = " ".join(args)
            reportChannelId = database.getGuildReport(ctx.guild.id)
            reportChannel = self.bot.get_channel(reportChannelId)
            pfp = ctx.message.author.avatar_url
            embed = discord.Embed(title="New Report")
            embed.set_author(name=ctx.author, icon_url=pfp)
            embed.color = discord.Color.from_rgb(213, 0, 30)
            embed.description = msgContent
            userInfo = self.userInfoGenerator(ctx.message.author, ctx.channel.id, ctx)
            embed.add_field(name="User info",value=userInfo, inline=True)
            if len(ctx.message.mentions) >= 1:
                x = 1
                for mention in ctx.message.mentions:
                    mentionInfo = self.mentionInfoGenerator(mention)
                    embed.add_field(name="Mentioned user #{}".format(x), value=mentionInfo, inline=True) 
                    x += 1
            footer_time = time.strftime('%m/%d/%Y', time.localtime())
            embed.set_footer(text="Author ID: {} • {}".format(ctx.author.id, footer_time))
            await reportChannel.send(embed=embed)
            
    def userInfoGenerator(self, user, channelID, ctx):
        joinedMsg = self.getTimeSince(user.joined_at)
        createdMsg = self.getTimeSince(user.created_at)
        jumpToContext = "<#{}> [Jump to context]({})".format(channelID, ctx.message.jump_url)
        returnMsg = "**Name:** {} {}\n**Joined:** {}\n**Created:** {}\n**Sent from:** {}".format(user, ctx.author.mention, joinedMsg, createdMsg, jumpToContext)
        return returnMsg
    def mentionInfoGenerator(self, user):
        joinedMsg = self.getTimeSince(user.joined_at)
        createdMsg = self.getTimeSince(user.created_at)
        return "**Name:** {} {}\n**Joined:** {}\n**Created:** {}\n**ID:** {}".format(user, user.mention, joinedMsg, createdMsg, user.id)
    def getTimeSince(self, user):
        returnMsg = ""
        timestamp = user.timestamp()
        timeLive = time.time() - timestamp
        years = 0 #365 day years (31536000)
        months = 0 #30 day months(2592000)
        days = 0 #86400 in a day
        hours = 0 #3600 in an hour
        minutes = 0 #60 in a minute
        while timeLive >= 31536000:
            years = years + 1
            timeLive = timeLive - 31536000
        while timeLive >= 2592000:
            months += 1
            timeLive -= 2592000
        while timeLive >= 86400:
            days += 1
            timeLive -= 86400
        while timeLive >= 3600:
            hours += 1
            timeLive -= 3600
        while timeLive >= 60:
            minutes += 1
            timeLive -= 60
        if years > 0:
            if months > 0:
                if days > 0:
                    returnMsg = "{} years, {} months and {} days ago".format(years, months, days)
                elif hours > 0:
                    returnMsg = "{} years, {} months and {} hours ago".format(years, months, hours)
                elif minutes > 0:
                    returnMsg = "{} years, {} months and {} minutes ago".format(years, months, minutes)
                else:
                    returnMsg = "{} years, {} months and {} seconds ago".format(years, months, timeLive)
            elif days > 0:
                if hours > 0:
                    returnMsg = "{} years, {} days and {} hours ago".format(years, days, hours)
                elif minutes > 0:
                    returnMsg = "{} years, {} days and {} minutes ago".format(years, days, minutes)
                else:
                    returnMsg = "{} years, {} days and {} seconds ago".format(years, days, timeLive)
            elif hours > 0:
                if minutes > 0:
                    returnMsg = "{} years, {} hours and {} minutes ago".format(years, hours, minutes)
                else:
                    returnMsg = "{} years, {} hours and {} seconds ago".format(years, hours, timeLive)
            elif minutes > 0:
                returnMsg = "{} years, {} minutes and {} seconds ago".format(years, minutes, timeLive)
            else:
                returnMsg = "{} years and {} seconds ago".format(years, timeLive)
        elif months > 0:
            if days > 0:
                if hours > 0:
                    returnMsg = "{} months, {} days and {} hours ago".format(months, days, hours)
                elif minutes > 0:
                    returnMsg = "{} months, {} days and {} minutes ago".format(months, days, minutes)
                else:
                    returnMsg = "{} months, {} days and {} seconds ago".format(months, days, timeLive)
            elif hours > 0:
                if minutes > 0:
                    returnMsg = "{} months, {} hours and {} minutes ago".format(months, hours, minutes)
                else:
                    returnMsg = "{} months, {} hours and {} seconds ago".format(months, hours, timeLive)
            elif minutes > 0:
                returnMsg = "{} months, {} minutes and {} seconds ago".format(months, minutes, timeLive)
            else:
                returnMsg = "{} months and {} seconds ago".format(months, timeLive)
        elif days > 0:
            if hours > 0:
                if minutes > 0:
                    returnMsg = "{} days, {} hours and {} minutes ago".format(days, hours, minutes)
                else:
                    returnMsg = "{} days, {} hours and {} seconds ago".format(days, hours, timeLive)
            elif minutes > 0:
                returnMsg = "{} days, {} minutes and {} seconds ago".format(days, minutes, timeLive)
            else:
                returnMsg = "{} days and {} seconds ago".format(days, timeLive)
        elif hours > 0:
            if minutes > 0:
                returnMsg = "{} hours, {} minutes and {} seconds ago".format(hours, minutes, timeLive)
            else:
                returnMsg = "{} hours and {} seconds ago".format(hours, timeLive)
        elif minutes > 0:
            returnMsg = "{} minutes and {} seconds ago".format(minutes, timeLive)
        else:
            returnMsg = "{} seconds ago".format(timeLive)
        return returnMsg
def setup(bot):
    bot.add_cog(Reports(bot))