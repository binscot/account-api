"""Pytest fixtures."""

import pytest
from beanie import init_beanie
from httpx import AsyncClient
from motor import motor_asyncio

from app.core.config import settings
from app.main import app
from app.schemas.user_schema import User, UserShort

MONGO_SERVER_URL = settings.MONGO_SERVER_URL
MONGO_TEST_DB_NAME = settings.MONGO_TEST_DB_NAME


async def mock_database():
    mongo_client = motor_asyncio.AsyncIOMotorClient(f"mongodb://{MONGO_SERVER_URL}")
    await init_beanie(
        database=mongo_client[MONGO_TEST_DB_NAME],
        recreate_views=True,
        document_models=[User, UserShort],
    )
    return mongo_client


@pytest.fixture(scope="function")
async def test_client():
    # Create an AsyncClient instance to make requests to the FastAPI api
    async with AsyncClient(app=app, base_url="http://test", follow_redirects=True) as ac:
        yield ac


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="function", autouse=False)
async def initialized_db():
    # Initialize the database and return the client
    client = await mock_database()
    yield client
    client.close()


@pytest.fixture(scope="function", autouse=False)
async def initialized_and_drop_db():
    # Initialize the database and return the client
    client = await mock_database()
    yield client
    # Teardown - clean up the database after each test
    await client.drop_database(MONGO_TEST_DB_NAME)
    print('test db drop')
    client.close()
