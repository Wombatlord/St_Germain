import aiohttp
from typing import Optional, Dict


async def getResponseBody(url: str) -> Optional[dict]:
    """
    Gets a resource at url and parses the json body to a dict,
    returns None on failed backend.
    @param url:
    @return:
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                return None
            body = await response.json()

    return body


async def downloadFile(url: str) -> Optional[bytes]:
    """
    Downloads a file at url, returns None on failed backend.
    @param url:
    @return:
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                return None
            filestream = await response.read()

    return filestream


async def getFullDeck() -> Optional[dict]:
    url = "https://rws-cards-api.herokuapp.com/api/v1/cards/"
    return await getResponseBody(url)


async def getRandomCards(number: int) -> Optional[dict]:
    url = f"https://rws-cards-api.herokuapp.com/api/v1/cards/random?n={number}"
    return await getResponseBody(url)


async def downloadCardImage(card: Dict[str, str]) -> Optional[bytes]:
    url = "https://www.sacred-texts.com/tarot/pkt/img/{}.jpg".format(card["name_short"])
    return await downloadFile(url)
