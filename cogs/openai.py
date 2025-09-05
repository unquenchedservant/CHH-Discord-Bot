from discord.ext import commands
import discord
from discord.commands import Option, slash_command
from utilities import openai

class OpenAI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        
        default_permissions=True,
        description="Ask CHHBot a question (Beta)",
    )
    async def ask(self, ctx: discord.ApplicationContext, prompt: Option(str, 'Prompt for CHHBot')):
        async with ctx.channel.typing():
            await ctx.defer()
            response = openai.generate_answer(prompt)
            await ctx.respond(response)
def setup(bot):
    bot.add_cog(OpenAI(bot))