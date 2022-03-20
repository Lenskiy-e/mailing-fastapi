import pytest
from config import settings
from models.group import Phone

headers = {
    'auth-key': settings.internal_auth_key
}


@pytest.mark.asyncio
async def test_phone_delete(api_client, get_connection):
    phone = "0999999941"
    phone_to_delete = "0999999942"
    new_group = {
        "name": "from pytest 9",
        "phones": [
            phone,
            phone_to_delete
        ]
    }

    response = await api_client.post("/group/", headers=headers, json=new_group)
    group_id = response.json().get('group_id')
    phone = get_connection.query(Phone).filter(Phone.phone == f'38{phone_to_delete}').first()

    delete_response = await api_client.delete(f"/phone/{phone.id}", headers=headers)
    phones = get_connection.query(Phone).filter(Phone.group_id == group_id).all()
    deleted_phone = get_connection.query(Phone).filter(Phone.phone == f'38{phone_to_delete}').first()

    assert delete_response.status_code == 200
    assert len(phones) == 1
    assert deleted_phone is None
