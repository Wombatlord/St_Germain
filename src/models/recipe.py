from __future__ import annotations
from typing import Tuple, List
import json


class Recipe:
    def __init__(
            self, author: str, title: str, ingredients: dict[str: str], cookTime: str,
            method: List[Tuple[int, str]], serves: int,
    ) -> None:
        self.author = author
        self.title = title
        self.ingredients = ingredients
        self.cookTime = cookTime
        self.method = method
        self.serves = serves

    async def setTitle(self, newTitle):
        self.title = newTitle

    async def setIngredient(self, newIngredient):
        self.ingredients = (1, newIngredient)

    async def getAuthor(self) -> str:
        return self.author

    async def getTitle(self) -> str:
        return self.title

    async def getIngredients(self) -> str:
        return self.ingredients

    async def getCookTime(self) -> str:
        return self.cookTime

    async def getMethod(self) -> List[Tuple[int, str]]:
        return self.method

    async def getServes(self) -> int:
        return self.serves

    async def serialize(self) -> str:
        recipeDict = {
            "author": self.author,
            "title": self.title,
            "ingredients": self.ingredients,
            "cookTime": self.cookTime,
            "method": self.method,
            "serves": self.serves,
        }

        return json.dumps(recipeDict)

    @classmethod
    async def deserialize(cls, jsonRecipe: str) -> Recipe:
        recipeDict = json.loads(jsonRecipe)
        return cls(**recipeDict)


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
