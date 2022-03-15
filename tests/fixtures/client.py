import pytest
from api.main import app
from httpx import AsyncClient


@pytest.fixture(scope='function')
async def api_client(anyio_backend) -> AsyncClient:
    try:
        async with AsyncClient(app=app, base_url="http://locahost") as ac:
            yield ac
    finally:
        pass
