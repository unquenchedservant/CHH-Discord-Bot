from discord.ext import commands
import discord
from discord.commands import Option, slash_command
from utilities import openai

class OpenAI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_answer(self, ctx, prompt):
        if not ctx.user.global_name == None:
            uname = ctx.user.global_name
        elif not ctx.user.nick == None:
            uname = ctx.user.nick
        else:
            uname = ctx.user.name
        return openai.generate_answer(prompt, uname=uname)
    
    @slash_command(
        
        default_permissions=True,
        description="Ask CHHBot a question (Beta)",
    )
    async def ask(self, ctx: discord.ApplicationContext, prompt: Option(str, 'Prompt for CHHBot', required=True), hide: Option(bool, "Do you want this to show only for you?", required=False, default=False)):
        print(f"THIS IS THE HIDE VALUE {hide}")
        await ctx.defer(ephemeral=hide)
        if not hide:
            async with ctx.channel.typing():
                response = self.get_answer(ctx, prompt)
        else:
            response = self.get_answer(ctx, prompt)
        print(f"THIS IS THE HIDE2 VALUE {hide}")
        await ctx.respond(response, ephemeral=hide)
def setup(bot):
    bot.add_cog(OpenAI(bot))