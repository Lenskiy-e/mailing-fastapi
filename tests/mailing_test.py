import pytest
from random import randint
from config import settings

headers = {
    'auth-key': settings.internal_auth_key
}


@pytest.mark.asyncio
async def test_mailing_create(api_client):
    new_group = await create_group(api_client, prepare_group())
    group_id = new_group.json().get('group_id')
    mailing_data = {
        "name": "valid name",
        "alpha_name": "alpha name",
        "group_id": group_id,
        "message": "valid message",
        "scheduled_at": "2022-04-17 11:25:47"
    }

    response = await create_mailing(api_client, mailing_data)
    mailing = response.json()

    assert response.status_code == 201
    assert 'id' in mailing


def prepare_group() -> dict:
    return {
        "name": f"from pytest mailing {randint(10,30)}",
        "phones": [
            f"09999999{randint(54,99)}"
        ]
    }


async def create_group(api_client, request_data: dict):
    return await api_client.post("/group/", headers=headers, json=request_data)


async def create_named_group(api_client, request_data: dict):
    return await api_client.post("/group/named", headers=headers, json=request_data)


async def create_mailing(api_client, request_data: dict):
    return await api_client.post("/mailing", headers=headers, json=request_data)
