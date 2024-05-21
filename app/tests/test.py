"""User information tests."""

import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_user_get(client_test: AsyncClient) -> None:
    """Test user endpoint returns authorized user."""
    resp = await client_test.post("/api/v1/account/signup", json={
        "username": "test8@gmail.com",
        "join_type": "tesjoin",
        "service_type": "test service",
        "password1": "string",
        "password2": "string"
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data == {
        "success": True,
        "message": None,
        "data": "test8@gmail.com",
        "request": "test8@gmail.com"
    }
