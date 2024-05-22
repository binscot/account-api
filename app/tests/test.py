"""User information tests."""

import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_user_get(client_test: AsyncClient) -> None:
    """Test user endpoint returns authorized user."""
    resp = await client_test.post("/api/v1/account/signup", json={
        "username": "test@gmail.com",
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
        "data": "test@gmail.com",
        "request": "test@gmail.com"
    }


@pytest.mark.anyio
async def test_perform_login(client_test: AsyncClient) -> None:
    """Test user endpoint returns authorized user."""
    login_resp_ = await client_test.post("/api/v1/account/signin", data={
        "username": "test@gmail.com",
        "password": "string",
    }, headers={"content-type": "application/x-www-form-urlencoded"})
    assert login_resp_.status_code == 200
    login_data = login_resp_.json()
    login_data = login_data["data"]
    assert "access_token" in login_data
    assert "username" in login_data
    print("login success")

    access_token = login_data["access_token"]
    authorization = f"bearer {access_token}"
    get_me_resp = await client_test.get("/api/v1/account/me", headers={
        "Authorization": authorization
    })

    assert get_me_resp.status_code == 200
    print(get_me_resp)
    get_me_resp = get_me_resp.json()
    get_me_data = get_me_resp["data"]
    assert "test@gmail.com" == get_me_data["username"]
    print("get me success")

    update_resp = await client_test.put(
        "/api/v1/account/update",
        json={
            "gender": "man",
            "birthday": "19900317",
            "phone_number": "010",
            "original_password": "string",
            "new_password": "test_string",
            "new_password_check": "test_string"

        },
        headers={
            "Authorization": authorization
        }
    )
    assert update_resp.status_code == 200
    print(update_resp)
    update_resp = update_resp.json()
    update_data = update_resp["data"]
    assert "man" == update_data["gender"]
    assert "19900317" == update_data["birthday"]
    """
    TODO 재 로그인으로 비밀번호 수정 확인
    """
    print("update test success")

    delete_resp = await client_test.delete("/api/v1/account/delete", headers={
        "Authorization": authorization
    })
    assert delete_resp.status_code == 200
    delete_resp = delete_resp.json()
    delete_data = delete_resp["data"]
    assert "test@gmail.com" == delete_data["username"]
    print(delete_resp["message"])

