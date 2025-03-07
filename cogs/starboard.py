from discord.ext import commands
import utilities
from utilities.logging import logger

class Starboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        true_count = 0
        if payload.emoji.name == "⭐":
            msg = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
            for reaction in msg.reactions:
                if reaction.emoji == "⭐":
                    if reaction.count >= 1:
                        true_count = reaction.count
                        #users = [user async for user in reaction.users()]
                        #for user in users:
                            # if user.bot:
                            #     print("Bot reacts don't count")
                            #     return
                            # if not user.id == msg.author.id:
                            #     if reaction.emoji == "⭐":
                            #         true_count += 1
                        if true_count >= 1:
                            logger.debug("Starboard")
                            starboard = self.bot.get_channel(utilities.get_starboard_channel())
                            await starboard.send(
                                f"**{msg.author.display_name}** in **{msg.channel.name}**\n{msg.content}"
                            )
                            return

def setup(bot):
    bot.add_cog(Starboard(bot))
