import pytest
from models.group import Group
from models.group import Phone
from config import settings
import os

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
async def test_group_create(api_client, get_connection):
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
    group = get_connection.query(Group).filter(Group.name == new_group.get('name')).first()
    phone = get_connection.query(Phone).filter(Phone.phone == f'38{valid_phone}').first()

    assert response.status_code == 201
    assert result.get('count') == 1
    assert result.get('result') == 'Created'
    assert result.get('group_id') == group.id
    assert result.get('group_id') == phone.group_id
    assert result.get('invalid') == [f'{invalid_phone} (invalid)', f'{valid_phone} (duplicate)']


@pytest.mark.asyncio
async def test_group_get_by_id(api_client, get_connection):
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
async def test_create_named_group(api_client, get_connection):
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
    group = get_connection.query(Group).filter(Group.id == result.get('group_id')).first()
    phone = get_connection.query(Phone).filter(Phone.group_id == result.get('group_id')).first()

    assert response.status_code == 201
    assert result.get('result') == 'Created'
    assert group.is_named is True
    assert group.name == new_named_group.get('name')
    assert group.description == new_named_group.get('description')
    assert phone.name == valid_phone.get('name')
    assert phone.phone == int(f"38{valid_phone.get('phone')}")
    assert result.get('invalid') == [
        f"{invalid_phone.get('phone')},{invalid_phone.get('name')} (invalid)",
        f"{invalid_name.get('phone')},{invalid_name.get('name')} (invalid)",
        f"{valid_phone.get('phone')},{valid_phone.get('name')} (duplicate)",
    ]


@pytest.mark.asyncio
async def test_update_group(api_client, get_connection):
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
            "0999999920",
            "9999999920"
        ]
    }
    response = await create_group(api_client, new_group)
    result = response.json()
    group_id = result.get('group_id')

    update_response = await api_client.patch(f'/group/{group_id}', headers=headers, json=updated_group_data)
    update_result = update_response.json()
    group = get_connection.query(Group).filter(Group.id == result.get('group_id')).first()
    phones = get_connection.query(Phone).filter(Phone.group_id == result.get('group_id')).all()

    # Checking response
    assert update_response.status_code == 200
    assert update_result.get('result') == 'Updated'
    assert update_result.get('group_id') == group_id
    assert update_result.get('count') == 1

    # Checking DB
    assert group.name == updated_group_data.get('name')
    assert group.description == updated_group_data.get('description')
    assert len(phones) == 2


@pytest.mark.asyncio
async def test_update_named_group(api_client, get_connection):
    new_named_group = {
            "name": "from pytest 6",
            "description": "created from test 6",
            "phones": [
                {
                    "name": "valid name",
                    "phone": "0999999921"
                }
            ]
        }
    updated_group_data = {
        "name": "from pytest 6 updated",
        "description": "created from test 6 updated",
        "phones": [
            {
                "name": "new name",
                "phone": "0999999922"
            },
            {
                "name": "Invalid~~name",
                "phone": "0999999922"
            },
            {
                "name": "invalid phone",
                "phone": "9999999922"
            }
        ]
    }

    create_response = await create_named_group(api_client, new_named_group)
    created_result = create_response.json()
    group_id = created_result.get('group_id')

    update_response = await api_client.patch(f'/group/{group_id}/named', headers=headers, json=updated_group_data)
    update_result = update_response.json()
    group = get_connection.query(Group).filter(Group.id == group_id).first()
    phones = get_connection.query(Phone).filter(Phone.group_id == group_id).all()

    # Checking response
    assert create_response.status_code == 201
    assert update_response.status_code == 200
    assert update_result.get('result') == 'Updated'
    assert update_result.get('group_id') == group_id
    assert update_result.get('count') == 1

    # Checking db
    assert group.name == updated_group_data.get('name')
    assert group.description == updated_group_data.get('description')
    assert len(phones) == 2


@pytest.mark.asyncio
async def test_delete_group(api_client, get_connection):
    valid_phone = "0999999923"
    new_group = {
        "name": "from pytest 7",
        "description": "created from test",
        "phones": [
            valid_phone
        ]
    }

    created_group_response = await create_group(api_client, new_group)
    created_group_result = created_group_response.json()
    group_id = created_group_result.get('group_id')

    response = await api_client.delete(f'/group/{group_id}', headers=headers)
    group = get_connection.query(Group).filter(Group.id == group_id).first()
    phones = get_connection.query(Phone).filter(Phone.group_id == group_id).all()

    assert response.status_code == 200
    assert group is None
    assert phones == []


@pytest.mark.asyncio
async def test_create_group_with_invalid_data(api_client):
    new_group = {
        "description": "created from test",
        "phones": [
            "0999999924"
        ]
    }
    response = await create_group(api_client, new_group)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_named_group_with_invalid_data(api_client):
    new_group = {
        "description": "created from test",
        "phones": [
            {
                "name": "valid name",
                "phone": "0999999925"
            }
        ]
    }
    response = await create_named_group(api_client, new_group)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_update_group_with_invalid_data(api_client, get_connection):
    new_group = {
        "name": "from pytest 8",
        "description": "created from test",
        "phones": [
            "0999999926"
        ]
    }

    update_data = {
        "description": "created from test",
        "phones": [
            "0999999927"
        ]
    }

    created_response = await create_group(api_client, new_group)
    group_id = created_response.json().get('group_id')

    update_response = await api_client.patch(f'/group/{group_id}', headers=headers, json=update_data)
    group = get_connection.query(Group).filter(Group.id == group_id).first()
    phones = get_connection.query(Phone).filter(Phone.group_id == group_id).all()

    assert update_response.status_code == 422
    assert group.name == new_group.get('name')
    assert group.description == new_group.get('description')
    assert len(phones) == 1


@pytest.mark.asyncio
async def test_update_named_group_with_invalid_data(api_client, get_connection):
    new_group = {
        "name": "from pytest 8",
        "description": "created from test",
        "phones": [
            {
                "name": "valid name",
                "phone": "0999999928"
            }
        ]
    }

    update_data = {
        "description": "created from test",
        "phones": [
            {
                "name": "valid name",
                "phone": "0999999929"
            }
        ]
    }

    created_response = await create_named_group(api_client, new_group)
    group_id = created_response.json().get('group_id')

    update_response = await api_client.patch(f'/group/{group_id}/named', headers=headers, json=update_data)
    group = get_connection.query(Group).filter(Group.id == group_id).first()
    phones = get_connection.query(Phone).filter(Phone.group_id == group_id).all()

    assert update_response.status_code == 422
    assert group.name == new_group.get('name')
    assert group.description == new_group.get('description')
    assert len(phones) == 1


@pytest.mark.asyncio
async def test_get_undefined_group(api_client):
    response = await api_client.get('/group/1234456', headers=headers)

    assert response.status_code == 404
    assert response.json() == {'detail': 'Group not found'}


@pytest.mark.asyncio
async def test_update_undefined_group(api_client, get_connection):
    undefined_phone = "0999999930"
    update_data = {
        "name": "undefined group",
        "description": "This group is undefined",
        "phones": [
            undefined_phone
        ]
    }
    group_id = 123123123

    response = await api_client.patch(f'/group/{group_id}', headers=headers, json=update_data)
    group = get_connection.query(Group).filter(Group.id == group_id).first()
    phone = get_connection.query(Phone).filter(Phone.phone == f'38{undefined_phone}').first()

    assert response.status_code == 404
    assert response.json() == {'detail': 'Group not found'}
    assert group is None
    assert phone is None


@pytest.mark.asyncio
async def test_update_undefined_named_group(api_client, get_connection):
    undefined_phone = {
        "phone": "0999999931",
        "name": "undefined name"
    }
    update_data = {
        "name": "undefined group",
        "description": "This group is undefined",
        "phones": [
            undefined_phone
        ]
    }
    group_id = 321321

    response = await api_client.patch(f'/group/{group_id}/named', headers=headers, json=update_data)
    group = get_connection.query(Group).filter(Group.id == group_id).first()
    phone = get_connection.query(Phone).filter(Phone.phone == f'38{undefined_phone.get("phone")}').first()

    assert response.status_code == 404
    assert response.json() == {'detail': 'Group not found'}
    assert group is None
    assert phone is None


@pytest.mark.asyncio
async def test_delete_undefined_group(api_client):
    response = await api_client.delete(f'/group/123123', headers=headers)

    assert response.status_code == 404
    assert response.json() == {'detail': 'Group not found'}


@pytest.mark.asyncio
async def test_phone_parse(api_client):
    valid_phones = [
        '0999999932',
        '0999999932',
        '0999999933',
        '0999999934',
        '0999999935',
        '0999999936'
    ]
    invalid_phones = [
        '9999999999',
        '999999ff99'
    ]
    invalid_phones_response = [
        '0999999932 (duplicate)',
        '9999999999 (invalid)',
        '999999ff99 (invalid)'
    ]
    valid_phones_response = [
        380999999932,
        380999999933,
        380999999934,
        380999999935,
        380999999936
    ]

    file_path = f'{os.path.dirname(os.path.abspath(__file__))}/phones.csv'

    f = open(file_path, "a")
    f.write('\n'.join(valid_phones + invalid_phones))
    f.close()

    file_for_parse = open(file_path, 'rb')

    response = await api_client.post('/group/parse_file', files={'file': file_for_parse})
    result = response.json()
    os.remove(file_path)

    assert response.status_code == 200
    assert result.get('valid') == valid_phones_response
    assert result.get('invalid') == invalid_phones_response


@pytest.mark.asyncio
async def test_named_phone_parse(api_client):
    valid_phones = [
        "0999999937,Альберт",
        "380999999938,Мар'ян",
        "380999999939,Ян",
        "0999999940,name",
        "0999999937,Another name",
    ]
    invalid_phones = [
        "380999999941,მაჰარაძე გეორგი ტენგიზოვიჩი",
        "0999999942,Абдурахма́н Гена́зович",
        "0999999943,``~`~"
    ]
    invalid_phones_response = [
        "0999999937,Another name (duplicate)",
        "380999999941,მაჰარაძე გეორგი ტენგიზოვიჩი (invalid)",
        "0999999942,Абдурахма́н Гена́зович (invalid)",
        "0999999943,``~`~ (invalid)"
    ]
    valid_phones_response = [
        {
            "name": "Альберт",
            "phone": "380999999937"
        },
        {
            "name": "Мар'ян",
            "phone": "380999999938"
        },
        {
            "name": "Ян",
            "phone": "380999999939"
        },
        {
            "name": "name",
            "phone": "380999999940"
        }
    ]

    file_path = f'{os.path.dirname(os.path.abspath(__file__))}/named_phones.csv'

    f = open(file_path, "a")
    f.write('\n'.join(valid_phones + invalid_phones))
    f.close()

    file_for_parse = open(file_path, 'rb')

    response = await api_client.post('/group/parse_named_file', files={'file': file_for_parse})
    result = response.json()
    os.remove(file_path)

    assert response.status_code == 200
    assert result.get('valid') == valid_phones_response
    assert result.get('invalid') == invalid_phones_response


async def create_group(api_client, new_group: dict):
    return await api_client.post("/group/", headers=headers, json=new_group)


async def create_named_group(api_client, new_group: dict):
    return await api_client.post("/group/named", headers=headers, json=new_group)
