from __future__ import annotations
import json
import random
from typing import Optional, Dict, Type
from src.adaptors.httpAdaptor import getResponseBody, downloadFile

HTTP: int = 0
FS: int = 1


def get(mode: int) -> Type[TarotRepository]:
    return [
        HttpTarotRepository,
        FSTarotRepository
    ][mode]


class TarotRepository:
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
    config: dict = {
        "host": "rws-cards-api.herokuapp.com/api",
        "scheme": "https"
    }

    @classmethod
    def _getApiRoot(cls):
        return f"{cls.config.get('scheme')}://{cls.config.get('host')}"

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
        url = "https://www.sacred-texts.com/tarot/pkt/img/{}.jpg".format(card["name_short"])
        return await downloadFile(url)


class FSTarotRepository(TarotRepository):
    """
    UNDER CONSTRUCTION
    """
    path: str = "assets/tarot.json"

    @classmethod
    def _decorateWithNhits(cls, cards):
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
