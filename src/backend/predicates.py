import discord
from discord.ext import commands


# Decorator for limiting commands per channel.
def inChannels(*args):
    def predicate(ctx):
        return ctx.message.channel.id in args

    return commands.check(predicate)


# This is responding with DM, not DM predicate.
# Just testing for later.
async def checkDM(ctx):
    if ctx.author.bot:
        return
    if isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.author.send("DM")
