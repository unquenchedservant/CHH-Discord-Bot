import os, discord, asyncio
from dotenv import load_dotenv

load_dotenv()

class chh_bot(discord.Client):

    async def on_ready(self):
        print("Logged on as {0}!".format(self.user))

    async def on_message(self, message):
        yes = "\U0001F4AF"
        no = "\U0001F6AB"
        ids = [702929735038271598, 685566940122447887, 365879579887534082]
        if message.author == self.user:
            return
        elif message.channel.id in ids:
            if (message.content.startswith("[SUBREDDIT]") or
                message.content.startswith("[DISCORD]") or
                message.content.startswith("[CHH]")):
                await message.add_reaction(yes)
                await message.add_reaction(no)
            else:
                for r in message.author.roles:
                    if not r.id == "613467520640221208":
                        await message.delete()
                        temp_message = await message.channel.send('%s please use [SUBREDDIT], [DISCORD] or [CHH] for your suggestions' % message.author.mention)
                        await asyncio.sleep(5)
                        await temp_message.delete()
                    else:
                        if message.content.startswith("^^clear"):
                            msgs = []
                            async for x in self.logs_from(message.channel, limit=number):
                                msgs.append(x)





client = chh_bot()
TOKEN=os.getenv('DISCORD_TOKEN')
client.run(TOKEN)
