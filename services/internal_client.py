import asyncio
import aiohttp
from aiohttp import ClientSession
from exceptions.internal_client import FailedRequestException, UnauthorizedException
from exceptions.security import AuthKeyHeaderNotFound
from config import settings
from typing import Optional
from fastapi import Header
from api.schemas.affiliate import AuthData

api_url = f'{settings.internal_api_url}/affiliates/info/by/token/'


def get_affiliate_id(auth_key: Optional[str] = Header(None)) -> int:
    if not auth_key:
        raise AuthKeyHeaderNotFound()

    return asyncio.run(auth(auth_key))[0]


def get_affiliate_auth_data(auth_key: Optional[str] = Header(None)) -> AuthData:
    if not auth_key:
        raise AuthKeyHeaderNotFound()
    
    return AuthData(
        affiliate_id=asyncio.run(auth(auth_key))[0],
        auth_key=auth_key
    )


def pay_for_sms(cost: float, auth_key: str) -> int:
    if not auth_key:
        raise AuthKeyHeaderNotFound()

    return 123


async def auth(token: str):
    headers = {
        'Auth-Role': settings.internal_api_role,
        'Access-Token': settings.internal_api_token
    }
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False), headers=headers) as session:
        response = asyncio.create_task(send_get_request(token, session))
        return await asyncio.gather(response)


async def send_get_request(token: str, session: ClientSession):
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
