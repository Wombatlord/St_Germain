from discord.ext.commands import Context
from typing import Iterable


async def sendDelimited(ctx: Context, message: str, delimiters: Iterable[str] = ("```",)) -> None:
    """
    Sends a message using the passed context with any delimiters specified.
    Delimiters should be provided as a tuple of strings, they are applied to
    the message sequentially such that the first supplied delimiter is the innermost.
    @param ctx:
    @param message:
    @param delimiters:
    """
    for delimiter in delimiters:
        message = delimiter + message + delimiter

    await ctx.send(message)
