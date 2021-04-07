from __future__ import annotations
from typing import List, Dict, Callable

import discord
from discord import Message
from discord.ext import commands
from discord.ext.commands import Context

# Embed colour field must be int. Convert a Hex colour value to an int before passing.
from src.models.recipe import Recipe

kindaGold = 16565763

testEmbed = {
    "title": "St. Germain's Kitchen",
    "description": "Choose an option to construct a recipe entry.",
    "color": 16565763,
    "fields": [
        {
            "name": "Options",
            "value": "1: Title\n 2: Ingredients\n 3: Cook Time\n 4: Method\n 5: Serves\n",
            "inline": True
        },
    ],
    "footer": {"text": "Cash Me Outside Howbow Dah"}
}

firstOptionEmbed = {
    "title": "Title your dish!",
    "description": "Type in a name for your recipe.",
    "colour": 1750068,

}

secondOptionEmbed = {
    "title": "Ingredients!",
    "description": "Type in an ingredient.",
    "colour": 1750068,

}

optionsList = ["1", "2", "3"]

embedded = discord.Embed.from_dict(testEmbed)
firstOptionEmbedded = discord.Embed.from_dict(firstOptionEmbed)
secondOptionEmbed = discord.Embed.from_dict(secondOptionEmbed)


class PrototypeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.optionList: List[int] = [1, 2, 3]

    @commands.command()
    async def newRecipe(self, ctx: Context) -> None:
        authorID: int = ctx.author.id
        newRecipe: Recipe = Recipe(author=ctx.author,
                                   title="",
                                   ingredients="",
                                   cookTime="",
                                   method=[],
                                   serves=4)

        await ctx.author.send(embed=embedded)

        def check(message) -> bool:
            print(authorID)
            print(message.author.id)
            return isinstance(message.channel, discord.channel.DMChannel) and message.author.id == authorID

        msg: Message = await self.bot.wait_for("message", check=lambda message: isinstance(message.channel,
                                                                                           discord.channel.DMChannel) and message.author.id == authorID)

        args = (self.bot, ctx, newRecipe, check)
        optionDict = {
            "1": lambda: supplyTitle(*args),
            "2": lambda: supplyIngredients(*args)
        }

        responder = optionDict.get(msg.content, lambda: ctx.author.message("Please choose either option 1 or option 2"))
        await responder()


async def supplyTitle(bot, ctx, newRecipe, check):
    await ctx.author.send(embed=firstOptionEmbedded)
    msg: Message = await bot.wait_for("message", check=check)

    newRecipe.setTitle(msg.content)
    await ctx.author.send(f"Recipe title is {newRecipe.title}!")


async def supplyIngredients(bot, ctx, newRecipe, check):
    await ctx.author.send(embed=secondOptionEmbed)
    msg: Message = await bot.wait_for("message", check=check)

    await newRecipe.setIngredient(msg.content)
    await ctx.author.send(f"Ingredient is {newRecipe.ingredients}!")


def setup(bot):
    cog = PrototypeCog(bot)

    bot.add_cog(cog)
