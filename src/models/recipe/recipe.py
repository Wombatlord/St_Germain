from __future__ import annotations
from typing import Tuple, List
import json


class Ingredient:
    def __init__(self, quantity: str, ingredient: str) -> None:
        self.quantity = quantity
        self.ingredient = ingredient

    def setQuantity(self, quantity):
        self.quantity = quantity

    def setIngredient(self, ingredient):
        self.ingredient = ingredient


class Recipe:
    def __init__(
            self, author: str, title: str, ingredients: List[Ingredient], cookTime: str,
            method: List[Tuple[int, str]], serves: int,
    ) -> None:
        self.author: str = author
        self.title: str = title
        self.ingredients: List[Ingredient] = ingredients
        self.cookTime: str = cookTime
        self.method: List[Tuple] = method
        self.serves: int = serves

    def addIngredient(self, ingredient: Ingredient) -> None:
        self.ingredients.append(ingredient)

    def setTitle(self, newTitle):
        self.title = newTitle

    def setIngredient(self, newIngredient):
        self.ingredients = newIngredient

    def setCookTime(self, cookTime):
        self.cookTime = cookTime

    def setMethod(self, method):
        self.method = method

    def setServes(self, serves):
        self.serves = serves

    def getAuthor(self) -> str:
        return self.author

    def getTitle(self) -> str:
        return self.title

    def getIngredients(self) -> List[Ingredient]:
        return self.ingredients

    def getCookTime(self) -> str:
        return self.cookTime

    def getMethod(self) -> List[Tuple[int, str]]:
        return self.method

    def getServes(self) -> int:
        return self.serves

    def getMethodJson(self) -> str:
        return json.dumps(self.getMethod())

    def getIngredientsText(self) -> str:
        return json.dumps(self.getIngredients())

    def serialize(self) -> str:
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
    def deserialize(cls, jsonRecipe: str) -> Recipe:
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
