from discord.ext import commands
import discord
from discord.commands import Option, slash_command
from utilities import openai

class OpenAI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_name(self, ctx):
        if not ctx.user.global_name == None:
            uname = ctx.user.global_name
        elif not ctx.user.nick == None:
            uname = ctx.user.nick
        else:
            uname = ctx.user.name
        return uname
    
    @slash_command(
        default_permissions=True,
        description="Ask CHHBot a question (Beta)",
    )
    async def ask(self, ctx: discord.ApplicationContext, prompt: Option(str, 'Prompt for CHHBot', required=True), hide: Option(bool, "Do you want this to show only for you?", required=False, default=False)):
        await ctx.defer(ephemeral=hide)
        uname = self.get_name(ctx)
        if not hide:
            async with ctx.channel.typing():
                response = openai.generate_answer(prompt, uname=uname)
                response = f"{uname} asked: \n{prompt}\n---\n" + response 
        else:
            response = openai.generate_answer(prompt, uname=uname)
        await ctx.respond(response, ephemeral=hide)
def setup(bot):
    bot.add_cog(OpenAI(bot))