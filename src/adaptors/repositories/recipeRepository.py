from __future__ import annotations

from typing import Optional, List, Union, Tuple

from src.adaptors.repositories.repository import Repository
from src.models.recipe import Recipe
from src.adaptors.database import db_adaptor as db


class RecipeRepository(Repository):
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
    def getByAuthor(cls, author: str) -> List[Recipe]:
        pass

    @classmethod
    def getByTitle(cls, title: str) -> Recipe:
        pass


class PostgresRecipeRepository(RecipeRepository):
    @classmethod
    def save(cls, recipe: Recipe) -> None:
        columnsString = ", ".join(list(cls.columns))
        values = [
            recipe.author,
            recipe.title,
            recipe.ingredients,
            recipe.cookTime,
            recipe.method,
            recipe.serves
        ]
        values = map(
            lambda v: f"'{v}'",
            values
        )
        valuesString = ", ".join(values)
        sql = f"INSERT INTO {cls.tableName} ({columnsString}) VALUES ({valuesString})"
        cursor = db.get_cursor()
        cursor.execute(sql)
        db.commit()

    @classmethod
    def getByID(cls, id: Union[str, int]) -> Optional[Recipe]:
        # TODO: Implement
        raise NotImplemented

    @classmethod
    def getByAuthor(cls, author: str) -> List[Recipe]:
        # TODO: Implement
        raise NotImplemented

    @classmethod
    def getByTitle(cls, title: str) -> Recipe:
        # TODO: Implement
        raise NotImplemented
