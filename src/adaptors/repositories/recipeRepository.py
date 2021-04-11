from __future__ import annotations

from typing import Optional, List, Union, Tuple

from src.adaptors.repositories.repository import Repository

from src.adaptors.database import db_adaptor as db
from src.models.recipe.recipe import Recipe


class RecipeRepository(Repository):
    @classmethod
    def getByAuthor(cls, author: str) -> List[Recipe]:
        pass

    @classmethod
    def getByTitle(cls, title: str) -> Recipe:
        pass


class PostgresRecipeRepository(RecipeRepository):
    tableName: str = "recipes"

    columns: Tuple = (
        "author",
        "title",
        "ingredients",
        "cook_time",
        "method",
        "serves"
    )

    @classmethod
    def save(cls, recipe: Recipe) -> None:
        columnsString = ", ".join(list(cls.columns))
        values = [
            recipe.author,
            recipe.title,
            recipe.getIngredientsText(),
            recipe.cookTime,
            recipe.getMethodJson(),
            recipe.serves
        ]
        placeholders = ", ".join(["%s"] * 6)
        sql = f"INSERT INTO {cls.tableName} ({columnsString}) VALUES ({placeholders})"
        print(sql)
        cursor = db.get_cursor()
        cursor.execute(sql, values)
        db.commit()

    @classmethod
    def getByID(cls, recipeID: Union[str, int]) -> Recipe:
        sql = f"SELECT * FROM recipes WHERE id = '{recipeID}'"
        cursor = db.get_cursor()
        cursor.execute(sql)
        row = cursor.fetchone()
        rowDict: dict = {
            "author": row[1],
            "title": row[2],
            "ingredients": row[3],
            "cookTime": row[4],
            "method": row[5],
            "serves": row[6],
        }
        recipe: Recipe = Recipe(**rowDict)
        return recipe

    @classmethod
    def getByAuthor(cls, author: str) -> Recipe:
        sql = f"SELECT * FROM recipes WHERE id = '{author}'"
        cursor = db.get_cursor()
        cursor.execute(sql)
        row = cursor.fetchone()
        rowDict: dict = {
            "author": row[0],
            "title": row[1],
            "ingredients": row[2],
            "cookTime": row[3],
            "method": row[4],
            "serves": row[5],
        }
        recipe: Recipe = Recipe(**rowDict)
        return recipe

    @classmethod
    def getByTitle(cls, title: str) -> Recipe:
        sql = f"SELECT * FROM recipes WHERE id = '{title}'"
        cursor = db.get_cursor()
        cursor.execute(sql)
        row = cursor.fetchone()
        rowDict: dict = {
            "author": row[0],
            "title": row[1],
            "ingredients": row[2],
            "cookTime": row[3],
            "method": row[4],
            "serves": row[5],
        }
        recipe: Recipe = Recipe(**rowDict)
        return recipe
