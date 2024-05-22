"""Pytest fixtures."""

import pytest
from asgi_lifespan import LifespanManager
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


async def clear_database(appa) -> None:
    print(appa)
    print(1)
    # await mongo_client.drop_database(MONGO_TEST_DB_NAME)
    # mongo_client.close()
    # print("DB 연결 종료되었습니다.")


@pytest.fixture
async def client_test(mocker):
    mongo_client = await mock_database()
    mocker.patch("app.core.database.MongoDBClient.connect", return_value=mongo_client)
    async with LifespanManager(app):
        app.mongo_client = mongo_client
        async with AsyncClient(app=app, base_url="http://test", follow_redirects=True) as _client:
            try:
                yield _client
            except Exception as exc:
                print(exc)



@pytest.fixture
def anyio_backend():
    return "asyncio"
