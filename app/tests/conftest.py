"""Pytest fixtures."""

import pytest
from asgi_lifespan import LifespanManager
from beanie import init_beanie
from fastapi import FastAPI
from httpx import AsyncClient
from mongomock_motor import AsyncMongoMockClient

from app.main import app
from app.schemas.user_schema import User, UserShort


async def mock_database():
    client = AsyncMongoMockClient()
    await init_beanie(
        database=client["pytest"],
        recreate_views=True,
        document_models=[User, UserShort],
    )


async def clear_database(server: FastAPI) -> None:
    """Empty the test database."""
    async for collection in await server.db.list_collections():  # type: ignore[attr-defined]
        await server.db[collection["users"]].delete_many({})  # type: ignore[attr-defined]


@pytest.fixture
async def client_test(mocker):
    """Async server client that handles lifespan and teardown."""
    print(mocker)
    mocker.patch("app.core.database.MongoDBClient.connect", return_value=await mock_database())
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://test", follow_redirects=True) as _client:
            try:
                yield _client
            except Exception as exc:
                print(exc)
            # finally:
            #     await clear_database(app)


@pytest.fixture
def anyio_backend():
    return "asyncio"
