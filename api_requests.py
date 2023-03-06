import aiohttp
from yarl import URL

from config import config


class ApiRequests:
    def __init__(self):
        self.session = aiohttp.ClientSession(base_url=URL(config['API_BASE_URL']))

    async def locate(self, url: str):
        url = f'/v1.9/locate?url={url}'

        async with self.session.get(url) as response:
            return await response.json() if response.ok else None

    async def subsite(self, url: str):
        located = await self.locate(url)
        if not located:
            return None
        subsite_id = located['result']['data']['id']

        url = f'/v1.9/subsite{subsite_id}'

        async with self.session.get(url) as response:
            return await response.json() if response.ok else None
