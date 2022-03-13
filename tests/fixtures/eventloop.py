import pytest
import asyncio


@pytest.fixture(scope='session', autouse=True)
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()
