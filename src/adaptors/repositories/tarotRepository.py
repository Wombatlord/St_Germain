from __future__ import annotations
import json
import random
from typing import Optional, Dict, Type
from src.adaptors.httpAdaptor import getResponseBody, downloadFile

# Repository Mode Select
HTTP: int = 0
FS: int = 1


def get(mode: int) -> Type[TarotRepository]:
    """
    Pass in a valid Mode Select to return the appropriate
    Repository interface.
    """
    return [
        HttpTarotRepository,
        FSTarotRepository
    ][mode]


class TarotRepository:
    """
    Generic interfaces for interacting with Tarot domain.
    Specific use case does not inherit from generic Repository class.
    """

    @classmethod
    async def getFullDeck(cls) -> Optional[dict]:
        pass

    @classmethod
    async def getRandomCards(cls, number: int) -> Optional[dict]:
        pass

    @classmethod
    async def getCardImage(cls, card: Dict[str, str]) -> Optional[bytes]:
        pass


class HttpTarotRepository(TarotRepository):
    """
    Implementations of generic Tarot interfaces.
    These implementations retrieve Tarot domain data over HTTP.
    This is the primary method by which the Tarot Cog retrieves cards.
    """
    config: dict = {
        "host": "rws-cards-api.herokuapp.com/api",
        "imageHost": "sacred-texts.com/tarot/pkt/img/{}.jpg",
        "scheme": "https"
    }

    @classmethod
    def _getApiRoot(cls):
        return f"{cls.config.get('scheme')}://{cls.config.get('host')}"

    @classmethod
    def _getImageRoot(cls):
        return f"{cls.config.get('scheme')}://{cls.config.get('imageHost')}"

    @classmethod
    async def getFullDeck(cls) -> Optional[dict]:
        url = f"{cls._getApiRoot()}/v1/cards/"
        return await getResponseBody(url)

    @classmethod
    async def getRandomCards(cls, number: int) -> Optional[dict]:
        url = f"{cls._getApiRoot()}/v1/cards/random?n={number}"
        return await getResponseBody(url)

    @classmethod
    async def getCardImage(cls, card: Dict[str, str]) -> Optional[bytes]:
        """
        A coincidence of naming convention allows an image to be retrieved
        from the imageHost simply by interpolating the 'name_short' property
        from the API or local JSON.
        A different image host is likely to require alternate implementation
        for url construction.
        """
        url = cls._getImageRoot().format(card["name_short"])
        return await downloadFile(url)


class FSTarotRepository(TarotRepository):
    """
    UNDER CONSTRUCTION
    Implementations of generic Tarot interfaces.
    These implementations interact with local filesystem to retrieve Tarot data.
    This is predominantly a backup method in case of Tarot API failure.
    Requires a local JSON copy of a Tarot deck (see Assets directory).
    HTTP is still used here for Image retrieval only.
    """
    path: str = "assets/tarot.json"

    @classmethod
    def _decorateWithNhits(cls, cards):
        """
        Returns a paginated tarot deck.
        :param cards: tarot JSON
        :return: dict containing a pagination field and the tarot JSON.
        """
        return {
            "nhits": len(cards),
            "cards": cards
        }

    @classmethod
    async def getFullDeck(cls) -> Optional[dict]:
        with open(cls.path) as reader:
            cards = json.loads(reader.read())

        return cls._decorateWithNhits(cards)

    @classmethod
    async def getRandomCards(cls, number: int) -> Optional[dict]:
        deck = await cls.getFullDeck()
        cardIndexList = random.sample(range(0, len(deck)), number)
        cards = map(
            lambda c: deck[c],
            cardIndexList
        )

        return cls._decorateWithNhits(list(cards))

    @classmethod
    async def getCardImage(cls, card: Dict[str, str]) -> Optional[bytes]:
        return await HttpTarotRepository.getCardImage(card)
