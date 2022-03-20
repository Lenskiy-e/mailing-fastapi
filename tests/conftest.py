import pytest
from sqlalchemy import MetaData
from db.database import engine
from db.database import get_db
from api.main import app
from httpx import AsyncClient


@pytest.fixture(scope='session')
def anyio_backend():
    return 'asyncio'


@pytest.fixture(scope='session', autouse=True)
async def setup_db():
    meta = MetaData()
    meta.reflect(bind=engine)
    meta.drop_all(bind=engine, checkfirst=True)
    engine.dispose()
    meta.create_all(bind=engine)


@pytest.fixture(scope='function')
def get_connection():
    return next(get_db())


@pytest.fixture(scope='function')
async def api_client(anyio_backend) -> AsyncClient:
    try:
        async with AsyncClient(app=app, base_url="http://locahost") as ac:
            yield ac
    finally:
        pass
