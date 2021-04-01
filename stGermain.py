import discord
import logging
from discord.ext import commands

from src.cogs.tarot import Tarot
from src.cogs.helper import Helper
from src.cogs.toys import Toy
from src.server import keepAlive, token
from src.backend import predicates
from src.recipes.recipe import respondForRecipe

# Bot setup.
logging.basicConfig()
description = 'St. Germain of The White Lodge'
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(
    command_prefix='!',
    description=description,
    intents=intents
)
bot.add_cog(Tarot(bot))
bot.add_cog(Helper(bot))
bot.add_cog(Toy(bot))

# Get correct API token path.
TOKEN = token.replOrLocal(token.repl, token.devFlag)

# Channel ID for inChannel check.
whiteLodgeChannel = 817823496352169985


@bot.event
async def on_ready():
    print('The veil is parted.')
    print(bot.user.name + ' ' + 'has arrived.')
    print('~*~*~*~*~*~*~*~*~*')
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="White Lodge Dreamers"
        )
    )


@bot.command()
async def createRecipe(ctx, *, message=''):
    await respondForRecipe(ctx, message)


@bot.listen()
async def on_message(ctx):
    await predicates.checkDM(ctx)


if token.repl is True:
    keepAlive.keepAlive()

bot.run(TOKEN)
