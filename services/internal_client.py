import asyncio
import aiohttp
from aiohttp import ClientSession
from exceptions.internal_client import FailedRequestException, UnauthorizedException
from config import settings

api_url = f'{settings.internal_api_url}/affiliates/info/by/token/'


async def auth(token: str):
    headers = {
        'Auth-Role': settings.internal_api_role,
        'Access-Token': settings.internal_api_token
    }
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False), headers=headers) as session:
        response = asyncio.create_task(send_request(token, session))
        return await asyncio.gather(response)


async def send_request(token: str, session: ClientSession):
    params = {
        'token': token
    }

    async with session.get(url=api_url, params=params) as response:
        response = await response.json()

        if not response.get('status'):
            raise FailedRequestException

        if response.get('status') != 'ok':
            raise UnauthorizedException

        return response.get('id')
