import pytest
from db.database import Base, engine, SessionLocal
from db.database import get_db


@pytest.fixture(scope='session', autouse=True)
async def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


@pytest.fixture(scope='function')
def get_connection():
    return next(get_db())
