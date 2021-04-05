from typing import Optional, Union, Any, List

from src.cogs.recipe import Recipe


class Repository:
    @classmethod
    def save(cls, entity: Any) -> None:
        pass

    @classmethod
    def getByID(cls, id: Union[str, int]) -> Optional[Any]:
        pass

    @classmethod
    def getAll(cls, limit: int = 10, offset: int = 0) -> List[Any]:
        pass
