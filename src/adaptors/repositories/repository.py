from typing import Optional, Union, Any, List


class Repository:
    """
    Generic Repository interfaces.
    Repositories should generally inherit these methods and provide
    their own specific implementations.

    Repositories are the intermediary infrastructure between the domain layer
    and the data layer. Logic for interaction between these layers should be implemented
    in specific loosely coupled repositories.
    """
    @classmethod
    def save(cls, entity: Any) -> None:
        pass

    @classmethod
    def getByID(cls, id: Union[str, int]) -> Optional[Any]:
        pass

    @classmethod
    def getAll(cls, limit: int = 10, offset: int = 0) -> List[Any]:
        pass
