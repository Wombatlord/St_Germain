from __future__ import annotations
from typing import Tuple, List
from discord.ext import commands
from discord.ext.commands import Context
import json


class Recipe():
    def __init__(
            self, bot, ctx: Context, title: str, ingredients: dict[str: str], cookTime: str,
            method: List[Tuple[int, str]], serves: int,
    ) -> None:
        self.bot = bot
        self._author = ctx.author
        self._title = title
        self._ingredients = ingredients
        self._cookTime = cookTime
        self._method = method
        self._serves = serves

    @property
    async def author(self) -> str:
        return self._author

    @property
    async def title(self) -> str:
        return self._title

    @property
    async def ingredients(self) -> str:
        return self._ingredients

    @property
    async def cookTime(self) -> str:
        return self._cookTime

    @property
    async def method(self) -> List[Tuple[int, str]]:
        return self._method

    @property
    async def serves(self) -> int:
        return self._serves

    async def serialize(self) -> str:
        recipeDict = {
            "author": self._author,
            "title": self._title,
            "ingredients": self._ingredients,
            "cookTime": self._cookTime,
            "method": self._method,
            "serves": self._serves,
        }

        return json.dumps(recipeDict)

    @classmethod
    async def deserialize(cls, jsonRecipe: str) -> Recipe:
        recipeDict = json.loads(jsonRecipe)
        return cls(**recipeDict)

    @commands.Cog.listener()
    async def on_member_join(self):
        pass


async def respondForRecipe(ctx, message):
    newRecipe = Recipe
    response = "Please press 1 or 2"
    await ctx.author.send(response)


# author = "Bezos"
# title = "Bezos' Beanz"
# ingredients = {
#     "25": "Amazon Brand 'Bezos Beanz'",
#     "1": "Alphabet",
#     "26": "Spaghet",
#     "Some": "Salt"
# }
# cookTime = "Half an hour"
# method = [
#     (1, "get beanz"),
#     (2, "combine alphabet with spaghet"),
#     (3, "salt the spaghet"),
#     (4, "roast over open fire"),
#     (5, "enjoy the end of days brought to you by Amazon's own Bezos.")
# ]
# serves = 1
#
# recipe = Recipe(author, title, ingredients, cookTime, method, serves)
# serialized = recipe.serialize()
# deserialized = recipe.deserialize(serialized)
# print(deserialized.author)
# print(deserialized.method[1])