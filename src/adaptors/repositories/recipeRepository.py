from __future__ import annotations

from typing import Optional, List, Union

from src.adaptors.repositories.repository import Repository
from src.cogs.recipe import Recipe


class RecipeRepository(Repository):

    @classmethod
    def getByAuthor(cls, author: str) -> List[Recipe]:
        pass

    @classmethod
    def getByTitle(cls, title: str) -> Recipe:
        pass


class PostgresRecipeRepository(RecipeRepository):
    @classmethod
    def save(cls, recipe: Recipe) -> None:
        # TODO: Implement
        raise NotImplemented

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
