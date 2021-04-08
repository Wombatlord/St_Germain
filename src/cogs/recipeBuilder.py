from __future__ import annotations

import discord
from discord.ext import commands
from discord.ext.commands import Context

from src.models.recipe import recipeMenu
from src.models.recipe.recipe import Recipe


class RecipeBuilderCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def newRecipe(self, ctx: Context) -> None:
        authorID: int = ctx.author.id
        newRecipe: Recipe = Recipe(author=ctx.author,
                                   title="",
                                   ingredients="",
                                   cookTime="",
                                   method=[],
                                   serves=4)

        def check(message) -> bool:
            print(authorID)
            print(message.author.id)
            return isinstance(message.channel, discord.channel.DMChannel) and message.author.id == authorID

        await recipeMenu.optionsMenu(self.bot, ctx, newRecipe, check)


def setup(bot):
    cog = RecipeBuilderCog(bot)

    bot.add_cog(cog)
