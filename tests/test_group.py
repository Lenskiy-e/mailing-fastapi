import pytest
from .fixtures.client import api_client


headers = {
    'auth-key': 'o1EzzzurPdJMwSQtVYzD8iar'
}


@pytest.mark.anyio
async def test_add_group(api_client):
    response = await api_client.get('/group', headers=headers)
    assert response.status_code == 200
