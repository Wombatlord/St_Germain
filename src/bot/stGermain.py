import discord
import logging
from discord.ext.commands import Bot as BotBase
from src.server import token

PREFIX = "!"
OWNER_IDS = [122159928793104384]
TOKEN = token.replOrLocal(token.repl, token.devFlag)

logging.basicConfig()
description = 'St. Germain of The White Lodge'
intents = discord.Intents.default()
intents.members = True


class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.guild = None
        self.TOKEN = TOKEN
        self.theRoomID = 402955354968948738
        self.wlTestingID = 815784988917235763

        super().__init__(
            command_prefix=self.PREFIX,
            owner_ids=OWNER_IDS,
            description=description,
            intents=intents,
        )

    def run(self):
        super().run(self.TOKEN, reconnect=True)

    async def on_connect(self):
        print("Bot connected")

    async def on_disconnect(self):
        print("Bot disconnected")

    async def on_ready(self):
        if token.repl is True:
            if not self.ready:
                self.ready = True
                self.guild = self.get_guild(self.theRoomID)

                print('The veil is parted.')
                print(bot.user.name + ' ' + 'has arrived.')
                print('~*~*~*~*~*~*~*~*~*')
                await bot.change_presence(
                    activity=discord.Activity(
                        type=discord.ActivityType.watching,
                        name="White Lodge Dreamers"
                    )
                )

        else:
            if not self.ready:
                self.ready = True
                self.guild = self.get_guild(self.wlTestingID)

                print('Welcome to The White Lodge Test Suite.')
                print(bot.user.name + ' ' + 'has arrived.')
                print('~*~*~*~*~*~*~*~*~*')
                await bot.change_presence(
                    activity=discord.Activity(
                        type=discord.ActivityType.watching,
                        name="Testing Magick"
                    )
                )


bot = Bot()

cogs = ["src.cogs.helper", "src.cogs.tarot", "src.cogs.toys"]
for cog in cogs:
    bot.load_extension(cog)

