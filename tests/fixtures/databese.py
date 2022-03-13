import pytest
from db.database import Base, engine, SessionLocal


@pytest.fixture(scope='session', autouse=True)
def setup_db(event_loop):
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
