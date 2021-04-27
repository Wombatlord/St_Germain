from __future__ import annotations

from typing import Optional, List, Union, Tuple

from src.adaptors.repositories.repository import Repository

from src.adaptors.database import db_adaptor as db
from src.models.recipe.recipe import Recipe, Ingredient


class RecipeRepository(Repository):
    @classmethod
    def getByAuthor(cls, author: str) -> List[Recipe]:
        pass

    @classmethod
    def getByTitle(cls, title: str) -> Recipe:
        pass


class PostgresRecipeRepository(RecipeRepository):
    tableName: str = "recipes"
    methodTable: str = "method"
    ingredientsTable: str = "ingredients"

    columns: Tuple = (
        "author",
        "title",
        "cook_time",
        "method",
        "serves"
    )

    @classmethod
    def save(cls, recipe: Recipe) -> None:
        cursor = db.get_cursor()

        def saveIngredient(ingredient_: Ingredient):
            ingredientSql = "INSERT INTO ingredients (ingredient, quantity, recipe_id) VALUES (%s, %s, %s)"
            cursor.execute(ingredientSql, [ingredient_.ingredient, ingredient_.quantity, recipe.id])

        methodString = "method"
        ingredientsString = "ingredients"
        columnsString = ", ".join(list(cls.columns))

        values = [
            recipe.author,
            recipe.title,
            recipe.cookTime,
            recipe.getMethodJson(),
            recipe.serves
        ]
        method = [recipe.getMethodJson()]
        # ingredients = [recipe.getIngredientsText()]

        placeholders = ", ".join(["%s"] * 5)
        placeholder = "%s"

        sql = f"INSERT INTO {cls.tableName} ({columnsString}) VALUES ({placeholders})"
        methodSql = f"INSERT INTO {cls.methodTable} ({methodString}) VALUES ({placeholder})"
        ingredientsSql = f"INSERT INTO {cls.ingredientsTable} ({ingredientsString}) VALUES ({placeholder})"

        print(sql)
        print(values)

        cursor.execute(sql, values)
        cursor.execute(methodSql, method)

        sqlRecipes = "INSERT INTO recipes (title) VALUES (%s)"
        cursor.execute(sqlRecipes, [recipe.title])
        for ingredient in recipe.ingredients:
            print(ingredient)
            saveIngredient(ingredient)
        # cursor.execute(ingredientsSql, ingredients)
        db.commit()

    @classmethod
    def _saveMethod(cls, recipe: Recipe) -> None:
        methodString = "method"
        value = [recipe.getMethodJson()]

        placeholder = "%s"
        sql = f"INSERT INTO {cls.methodTable} ({methodString}) VALUES ({placeholder})"
        print(sql)
        print(value)
        cursor = db.get_cursor()
        cursor.execute(sql, value)
        db.commit()

    @classmethod
    def _saveIngredients(cls, recipe: Recipe) -> None:
        ingredientsString = "ingredients"
        value = [recipe.getIngredientsText()]

        placeholder = "%s"
        sql = f"INSERT INTO {cls.ingredientsTable} ({ingredientsString}) VALUES ({placeholder})"
        cursor = db.get_cursor()
        cursor.execute(sql, value)
        db.commit()

    @classmethod
    def getByID(cls, recipeID: Union[str, int]) -> Recipe:
        sql = f"SELECT * FROM recipes WHERE recipe_id = '{recipeID}'"
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
