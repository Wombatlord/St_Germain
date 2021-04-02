from typing import Optional

import aiohttp


async def getResponseBody(url: str) -> Optional[dict]:
    """
    Gets a resource at url and parses the json body to a dict,
    returns None on failed utils.
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
    Downloads a file at url, returns None on failed utils.
    @param url:
    @return:
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                return None
            filestream = await response.read()

    return filestream
