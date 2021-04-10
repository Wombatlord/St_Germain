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
        placeholders = ", ".join(["%s"]*6)
        sql = f"INSERT INTO {cls.tableName} ({columnsString}) VALUES ({placeholders})"
        print(sql)
        cursor = db.get_cursor()
        cursor.execute(sql, values)
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
