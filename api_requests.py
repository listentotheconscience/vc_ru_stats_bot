import aiohttp
from yarl import URL

from config import config


class ApiRequests:
    def __init__(self):
        self.session = aiohttp.ClientSession(base_url=URL(config['API_BASE_URL']))

    async def locate(self, url: str):
        url = f'/v1.9/locate?url={url}'

        return await self._send_get_request(url)

    async def subsite(self, located: dict):
        subsite_id = located['result']['data']['id']
        url = f'/v1.9/subsite/{subsite_id}'

        return await self._send_get_request(url), subsite_id

    async def subsite_timeline(self, subsite_id: int):
        url = f'/v1.9/subsite/{subsite_id}/timeline/new'

        return await self._send_get_request(url)

    async def user(self, located: dict):
        user_id = located['result']['data']['id']
        url = f'/v1.9/user/{user_id}'

        return await self._send_get_request(url), user_id

    async def user_entries(self, user_id):
        url = f'/v1.9/user/{user_id}/entries'

        return await self._send_get_request(url)

    async def _send_get_request(self, url):
        async with self.session.get(url) as response:
            return await response.json() if response.ok else None
