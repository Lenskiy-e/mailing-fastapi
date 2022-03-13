import pytest
from .fixtures.databese import setup_db
from .fixtures.client import api_client
from .fixtures.eventloop import event_loop
from .fixtures.conftest import anyio_backend
from models.group import Group
from models.group import Phone

headers = {
    'auth-key': 'o1EzzzurPdJMwSQtVYzD8iar'
}


@pytest.mark.anyio
async def test_groups_get(api_client):
    response = await api_client.get("/group/", headers=headers)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_group_create(api_client, setup_db):
    new_phone = "0999999999"
    new_group = {
        "name": "from pytest",
        "phones": [
            new_phone
        ]
    }
    response = await create_group(api_client, new_group)
    result = response.json()
    group = setup_db.query(Group).filter(Group.name == new_group.get('name')).first()
    phone = setup_db.query(Phone).filter(Phone.phone == f'38{new_phone}').first()

    assert response.status_code == 201
    assert result.get('count') == 1
    assert result.get('invalid') == []
    assert result.get('result') == 'Created'
    assert result.get('group_id') == group.id
    assert result.get('group_id') == phone.group_id


async def create_group(api_client, new_group: dict):
    return await api_client.post("/group/", headers=headers, json=new_group)
