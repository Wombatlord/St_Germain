import discord
import logging
from discord.ext import commands

from src.cogs.tarotCog import Tarot
from src.server import keepAlive, token
from src.magicEight.magicEight import magicEightBall
from src.guidance.userGuide import userGuide
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

# Get correct API token path.
TOKEN = token.replOrLocal(token.repl, token.devFlag)

# Channel ID for inChannel check.
whiteLodgeChannel = 817823496352169985


# Decorator for limiting commands per channel.
def inChannels(*args):
    def predicate(ctx):
        return ctx.message.channel.id in args

    return commands.check(predicate)


async def checkDM(ctx):
    if ctx.author.bot:
        return
    if isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.author.send("DM")


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
async def guidance(ctx):
    await ctx.send(userGuide)


@bot.command()
async def add(ctx, left: int, right: int):
    # Adds two numbers
    await ctx.send(left + right)


@bot.command()
async def magicEight(ctx, *, message='question'):
    await magicEightBall(ctx, message)


@bot.command()
async def createRecipe(ctx, *, message=''):
    await respondForRecipe(ctx, message)


@bot.listen()
async def on_message(ctx):
    await checkDM(ctx)


if token.repl is True:
    keepAlive.keepAlive()

bot.run(TOKEN)
