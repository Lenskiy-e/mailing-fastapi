import pytest
from .fixtures.databese import setup_db
from .fixtures.client import api_client
from .fixtures.eventloop import event_loop
from .fixtures.conftest import anyio_backend
from models.group import Group
from models.group import Phone
from config import settings

headers = {
    'auth-key': settings.internal_auth_key
}


@pytest.mark.asyncio
async def test_groups_get(api_client):
    new_groups = [
        {
            "name": "from pytest 1",
            "phones": [
                "0999999911",
                "0999999912",
            ]
        },
        {
            "name": "from pytest 2",
            "phones": [
                "0999999913",
                "0999999914",
            ]
        }
    ]

    for group in new_groups:
        await create_group(api_client, group)

    response = await api_client.get("/group/", headers=headers)
    result = response.json()

    assert response.status_code == 200
    assert len(result) == 2
    assert result[0].get('name') == new_groups[0].get('name')
    assert result[1].get('name') == new_groups[1].get('name')


@pytest.mark.asyncio
async def test_group_create(api_client, setup_db):
    valid_phone = "0999999915"
    invalid_phone = "9999999999"
    new_group = {
        "name": "from pytest 3",
        "phones": [
            valid_phone,
            invalid_phone,
            valid_phone
        ]
    }
    response = await create_group(api_client, new_group)
    result = response.json()
    group = setup_db.query(Group).filter(Group.name == new_group.get('name')).first()
    phone = setup_db.query(Phone).filter(Phone.phone == f'38{valid_phone}').first()

    assert response.status_code == 201
    assert result.get('count') == 1
    assert result.get('result') == 'Created'
    assert result.get('group_id') == group.id
    assert result.get('group_id') == phone.group_id
    assert result.get('invalid') == [f'{invalid_phone} (invalid)', f'{valid_phone} (duplicate)']


@pytest.mark.asyncio
async def test_group_get_by_id(api_client, setup_db):
    new_phone = "0999999916"
    new_group = {
        "name": "from pytest 4",
        "description": "created from test",
        "phones": [
            new_phone
        ]
    }

    create_response = await create_group(api_client, new_group)
    created_group = create_response.json()
    created_group_id = created_group.get('group_id')

    response = await api_client.get(f'/group/{created_group_id}', headers=headers)
    result = response.json()

    assert response.status_code == 200
    assert result.get('id') == created_group_id
    assert result.get('name') == new_group.get('name')
    assert result.get('description') == new_group.get('description')
    assert result.get('phones')[0].get('phone') == int(f'38{new_phone}')
    assert not result.get('is_named')


@pytest.mark.asyncio
async def test_create_named_group(api_client, setup_db):
    valid_phone = {
        "name": "valid name",
        "phone": "0999999917"
    }
    invalid_phone = {
        "name": "valid name",
        "phone": "9999999999"
    }
    invalid_name = {
        "name": "~~~~.invalid Name",
        "phone": "0999999918"
    }

    new_named_group = {
        "name": "from pytest 4",
        "description": "created from test",
        "phones": [
            valid_phone,
            invalid_phone,
            invalid_name,
            valid_phone
        ]
    }

    response = await create_named_group(api_client, new_named_group)
    result = response.json()
    group = setup_db.query(Group).filter(Group.id == result.get('group_id')).first()
    phone = setup_db.query(Phone).filter(Phone.group_id == result.get('group_id')).first()

    assert response.status_code == 201
    assert result.get('result') == 'Created'
    assert group.is_named is True
    assert group.name == new_named_group.get('name')
    assert phone.name == valid_phone.get('name')
    assert phone.phone == int(f"38{valid_phone.get('phone')}")
    assert result.get('invalid') == [
        f"{invalid_phone.get('phone')},{invalid_phone.get('name')} (invalid)",
        f"{invalid_name.get('phone')},{invalid_name.get('name')} (invalid)",
        f"{valid_phone.get('phone')},{valid_phone.get('name')} (duplicate)",
    ]



@pytest.mark.asyncio
async def test_update_group(api_client, setup_db):
    new_group = {
        "name": "from pytest 5",
        "description": "created from test",
        "phones": [
            "0999999919"
        ]
    }
    updated_group_data = {
        "name": "from pytest 5 updated",
        "description": "created from test updated",
        "phones": [
            "0999999920"
        ]
    }
    response = await create_group(api_client, new_group)
    result = response.json()
    group_id = result.get('group_id')

    update_response = await api_client.patch(f'/group/{group_id}', headers=headers, json=updated_group_data)
    update_result = update_response.json()
    group = setup_db.query(Group).filter(Group.id == result.get('group_id')).first()
    phones = setup_db.query(Phone).filter(Phone.group_id == result.get('group_id')).all()

    # Checking response
    assert update_response.status_code == 200
    assert update_result.get('result') == 'Updated'
    assert update_result.get('group_id') == group_id
    assert update_result.get('count') == 1

    # Checking DB
    assert group.name == updated_group_data.get('name')
    assert group.description == updated_group_data.get('description')
    assert len(phones) == 2


async def create_group(api_client, new_group: dict):
    return await api_client.post("/group/", headers=headers, json=new_group)


async def create_named_group(api_client, new_group: dict):
    return await api_client.post("/group/named", headers=headers, json=new_group)
