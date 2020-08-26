import discord, os, re
from discord.ext import commands
from discord.utils import get
from utilities import database
from itertools import permutations

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
                    await message.add_reaction(no)
                    await channel.send("Sorry {}, your suggestion has been denied. {} will tell you why.".format(message.author.mention, user.mention))
                elif payload.emoji.name == yes:
                    await message.add_reaction(yes)
                    await channel.send("Good news, {}, your suggestion has been accepted".format(message.author.mention))

    @commands.Cog.listener()
    async def on_message(self, message):
        yes = "✅"
        no = "❌"
        if not message.author.id == self.bot.user.id:
            stick_guilds = [613464665661636648,365879579887534080]
            stick_channels = [747899054712946759, 742919732478607460]
            if message.guild.id in stick_guilds and not message.channel.id in stick_channels:
                check_stick = message.content
                if not check_stick == "<:STICK:743597072598433924>":
                    check_stick = check_stick.lower()
                    _RE_COMBINE_WHITESPACE = re.compile(r"\s+")
                    check_stick = _RE_COMBINE_WHITESPACE.sub(" ", check_stick).strip()
                    _RE_REMOVE_PUNCTUATION = re.compile(r"(?![\$\!])\W{P}")
                    check_stick = _RE_REMOVE_PUNCTUATION.sub("", check_stick)
                    if check_stick.count("$") > 1:
                        x = check_stick.count("$") - 1
                        check_stick = check_stick.replace("$", "", 1)
                    if check_stick.count("$") >= 1 and check_stick.count("s") >= 1:
                        check_stick = check_stick.replace("$", "")
                    if check_stick.count("s") > 1:
                        x = check_stick.count("s") - 1
                        check_stick = check_stick.replace("s", "", 1)
                    if check_stick.count("t") > 1:
                        x = check_stick.count("t") - 1
                        check_stick = check_stick.replace("t", "", 1)
                    if check_stick.count("i") > 1:
                        x = check_stick.count("i") - 1
                        check_stick = check_stick.replace("i", "", x)
                    if check_stick.count("!") > 1:
                        x = check_stick.count("!") - 1
                        check_stick = check_stick.replace("!", "", x)
                    if check_stick.count("!") >= 1 and check_stick.count("i") >= 1:
                        check_stick = check_stick.replace("!", "")
                    if check_stick.count("c") > 1:
                        x = check_stick.count("c") - 1
                        check_stick = check_stick.replace("c", "", x)
                    if check_stick.count("k") > 1:
                        x = check_stick.count("k") - 1
                        check_stick = check_stick.replace("k", "", x)
                if check_stick.count(" ") > 4:
                    print(check_stick)
                else:
                    check_stick = check_stick.replace(" ", "")
                    stick_found = False
                    if len(check_stick) < 10:
                        check_array = [''.join(p) for p in permutations(check_stick)]
                        for item in check_array:
                            result = re.match(r'^[s$S\*]\s*[\*Tt]\s*[\*1\|¡iIl]\s*[\*(Cc]\s*[\*kK]\W*$', item)
                            if result:
                                stick_found = True
                                break
                    if stick_found or message.content == "<:STICK:743597072598433924>" or message.content.lower() == "thtick":
                        await message.delete()
                        await message.channel.send("https://cdn.discordapp.com/emojis/746124789835497613.gif?v=1")
                    else:
                        print("not stick")
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
