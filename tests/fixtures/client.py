import pytest
from api.main import app
from httpx import AsyncClient


@pytest.fixture(scope='module')
async def api_client() -> AsyncClient:
    try:
        async with AsyncClient(app=app, base_url='http://localhost') as ac:
            yield ac
    finally:
        pass
