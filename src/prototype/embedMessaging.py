from __future__ import annotations
from typing import List

import discord
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
    async def newRecipe(self, ctx):
        authorID = ctx.author.id
        newRecipe: Recipe = Recipe(author=ctx.author,
                                   title="",
                                   ingredients="",
                                   cookTime="",
                                   method=[],
                                   serves=4)

        await ctx.author.send(embed=embedded)

        def check(message):
            return isinstance(message.channel, discord.channel.DMChannel)

        msg = await self.bot.wait_for("message", check=check)

        if msg.content == "1":
            await ctx.author.send(embed=firstOptionEmbedded)
            msg = await self.bot.wait_for("message", check=check)

            await newRecipe.setTitle(msg.content)
            await ctx.author.send(f"Recipe title is {newRecipe.title}!")

        if msg.content == "2":
            await ctx.author.send(embed=secondOptionEmbed)
            msg = await self.bot.wait_for("message", check=check)

            await newRecipe.setIngredient(msg.content)
            await ctx.author.send(f"Ingredient is {newRecipe.ingredients}!")

    @commands.command()
    async def embedTest(self, ctx, message):
        if ctx.author.bot:
            return
        if isinstance(ctx.channel, discord.channel.DMChannel):
            if message in optionsList:
                await ctx.author.send(embed=embedded)
            else:
                await ctx.author.send("Option not found.")


def setup(bot):
    bot.add_cog(PrototypeCog(bot))
