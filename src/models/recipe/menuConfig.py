
from typing import Callable, Coroutine, Any

import discord
from discord.ext.commands import Context

from src.bot.stGermain import Bot

Check = Callable[[discord.Message], bool]
SideEffectPromise = Coroutine[Any, Any, None]
InputNode = Callable[[Bot, Context], SideEffectPromise]
InputHandler = Callable[[Bot, Context, discord.Message], SideEffectPromise]


class NodeConfig:
    def __init__(self, prompt: discord.Embed, inputHandler: InputHandler, check: Check, completionHandler: Callable):
        self.prompt = prompt
        self.inputHandler = inputHandler
        self.check = check
        self.completionHandler = completionHandler

    def toDict(self):
        return {
            "prompt": self.prompt,
            "inputHandler": self.inputHandler,
            "check": self.check,
            "completionHandler": self.completionHandler
        }
