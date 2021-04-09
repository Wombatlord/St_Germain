from collections import Callable, Coroutine
from typing import Any, List, Union, Dict

import discord
from discord import Message
from discord.ext.commands import Context

from src.bot.stGermain import Bot
from src.models.recipe.menuConfig import NodeConfig, InputHandler, Check, InputNode

inputHandlers = {}
checks = {}
embeds = {}
inputNodeAssignments: Dict[str, Union[str, Dict[str, str], NodeConfig]] = {}
mainMenuPrompt = None
mainCheck = lambda x: True


def registerInputHandler(identifier):
    def decorator(func):
        inputHandlers[identifier] = func
        return func

    return decorator


def registerCheck(identifier):
    def decorator(func):
        checks[identifier] = func
        return func

    return decorator


def registerEmbed(embed, identifier):
    embeds[identifier] = embed


def configure(config):
    global inputNodeAssignments, mainMenuPrompt, mainCheck
    inputNodeAssignments = config["config"]
    mainMenuPrompt = config["prompt"]
    mainCheck = config["check"]


async def exitMenu(bot, ctx):
    await ctx.author.send("Exiting Recipe Creation.")


async def rootNode(bot, ctx):
    await menuNode(bot, ctx)


async def menuNode(bot, ctx):
    await ctx.author.send(embed=mainMenuPrompt)
    msg: Message = await bot.wait_for("message", check=mainCheck)

    optionDict = {}
    for key, value in inputNodeAssignments.items():
        isDict = isinstance(value, dict)
        isObject = isinstance(value, NodeConfig)
        if value == "exit":
            optionDict[key] = exitMenu
        elif isObject or isDict:
            value = value.toDict() if isObject else value
            optionDict[key] = inputNodeFactory(**value)
        else:
            optionDict[key] = inputNodeFactory(
                embeds[value],
                inputHandlers[value],
                checks[value],
                rootNode
            )

    error = lambda bot_, context: ctx.author.send("Please choose either option 1 or option 2")
    responder = optionDict.get(msg.content, None)

    if not responder:
        responderLambda = error
    else:
        responderLambda = lambda bot_, context: responder(bot_, context)

    await responderLambda(bot, ctx)


def inputNodeFactory(
        prompt: discord.Embed, inputHandler: InputHandler, check: Check, completionHandler: Callable
) -> InputNode:
    async def inputNode(bot: Bot, ctx: Context) -> None:
        await ctx.author.send(embed=prompt)
        msg: Message = await bot.wait_for("message", check=check)

        await inputHandler(bot, ctx, msg)
        await completionHandler(bot, ctx)

    return inputNode
