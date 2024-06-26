"""User tests."""

import re

import pytest


@pytest.mark.endpoint
@pytest.mark.anyio
@pytest.mark.parametrize("user", [
    {
        "username": "test@gmail.com",
        "join_type": "tesjoin",
        "service_type": "test service",
        "password1": "string",
        "password2": "string"
    }
])
async def test_signup_user(user, test_client, initialized_db):
    created_user = await test_client.post("/api/v1/account/signup", json=user)
    assert created_user.status_code == 200
    assert created_user.json() == {
        "success": True,
        "message": None,
        "data": "test@gmail.com",
        "request": "test@gmail.com"
    }

    print("signup success")


@pytest.mark.endpoint
@pytest.mark.anyio
@pytest.mark.parametrize("user", [
    {
        "username": "test@gmail.com",
        "password": "string",
    }
])
@pytest.mark.parametrize("headers", [
    {
        "content-type": "application/x-www-form-urlencoded"
    }
])
async def test_signin_user(user, headers, test_client, initialized_db):
    signin_user = await test_client.post("/api/v1/account/signin", data=user, headers=headers)
    assert signin_user.status_code == 200

    signin_user_json = signin_user.json()
    assert signin_user_json["success"]

    signin_user_data = signin_user_json["data"]
    token_data = signin_user_data["token_data"]
    signin_user_data = signin_user_data["user_data"]
    assert "access_token" in token_data
    assert "username" in signin_user_data
    assert signin_user_data["username"] == "test@gmail.com"
    print("signin success")


@pytest.mark.endpoint
@pytest.mark.anyio
@pytest.mark.parametrize("user", [
    {
        "username": "test@gmail.com",
        "password": "string",
    }
])
@pytest.mark.parametrize("headers", [
    {
        "content-type": "application/x-www-form-urlencoded"
    }
])
async def test_get_current_user(user, headers, test_client, initialized_db):
    signin_user = await test_client.post("/api/v1/account/signin", data=user, headers=headers)
    signin_user = signin_user.json()
    signin_user_data = signin_user["data"]
    token_data = signin_user_data["token_data"]
    account_info = await get_account_info(token_data["access_token"], test_client)
    assert account_info.status_code == 200

    account_info = account_info.json()
    account_info_data = account_info["data"]
    assert "test@gmail.com" == account_info_data["username"]

    print("get current user success")


@pytest.mark.endpoint
@pytest.mark.anyio
@pytest.mark.parametrize("user", [
    {
        "username": "test@gmail.com",
        "password": "string",
    }
])
@pytest.mark.parametrize("headers", [
    {
        "content-type": "application/x-www-form-urlencoded"
    }
])
async def test_reissue_token(user, headers, test_client, initialized_db):
    signin_user = await test_client.post("/api/v1/account/signin", data=user, headers=headers)
    assert signin_user.status_code == 200

    refresh_token = await get_refresh_token(signin_user)
    authorization = f"bearer {refresh_token}"
    get_reissue_token = await test_client.post("/api/v1/account/token/reissue", headers={
        "Authorization": authorization
    })
    assert get_reissue_token.status_code == 200
    new_token = get_reissue_token.json()
    new_token_data = new_token["data"]
    assert "access_token" in new_token_data

    access_token = new_token_data["access_token"]
    account_info = await get_account_info(access_token, test_client)
    assert account_info.status_code == 200

    account_info = account_info.json()
    account_info_data = account_info["data"]
    assert "test@gmail.com" == account_info_data["username"]

    print("get current user success")


@pytest.mark.endpoint
@pytest.mark.anyio
@pytest.mark.parametrize("user", [
    {
        "username": "test@gmail.com",
        "password": "string",
    }
])
@pytest.mark.parametrize("update_user", [
    {
        "gender": "man",
        "birthday": "19900317",
        "phone_number": "010",
        "original_password": "string",
        "new_password": "test_string",
        "new_password_check": "test_string"

    }
])
@pytest.mark.parametrize("headers", [
    {
        "content-type": "application/x-www-form-urlencoded"
    }
])
@pytest.mark.parametrize("update_user_signin", [
    {
        "username": "test@gmail.com",
        "password": "test_string",
    }
])
async def test_update_user(user, update_user, headers, update_user_signin, test_client, initialized_db):
    signin_user = await test_client.post("/api/v1/account/signin", data=user, headers=headers)
    signin_user_json = signin_user.json()
    signin_user_data = signin_user_json["data"]
    token_data = signin_user_data["token_data"]
    access_token = token_data["access_token"]
    authorization = f"bearer {access_token}"
    update_user = await test_client.put(
        "/api/v1/account/update",
        json=update_user,
        headers={
            "Authorization": authorization
        }
    )
    assert update_user.status_code == 200

    update_user = update_user.json()
    update_user_data = update_user["data"]
    assert "man" == update_user_data["gender"]
    assert "19900317" == update_user_data["birthday"]

    print("update test success")

    signin_user = await test_client.post("/api/v1/account/signin", data=update_user_signin, headers=headers)
    assert signin_user.status_code == 200


@pytest.mark.endpoint
@pytest.mark.anyio
@pytest.mark.parametrize("user", [
    {
        "username": "test@gmail.com",
        "password": "test_string",
    }
])
@pytest.mark.parametrize("headers", [
    {
        "content-type": "application/x-www-form-urlencoded"
    }
])
async def test_delete_user(user, headers, test_client, initialized_and_drop_db):
    signin_user = await test_client.post("/api/v1/account/signin", data=user, headers=headers)
    signin_user = signin_user.json()
    signin_user_data = signin_user["data"]
    token_data = signin_user_data["token_data"]
    access_token = token_data["access_token"]
    authorization = f"bearer {access_token}"
    delete_user = await test_client.delete("/api/v1/account/delete", headers={
        "Authorization": authorization
    })
    assert delete_user.status_code == 200

    delete_user = delete_user.json()
    delete_user_data = delete_user["data"]
    assert "test@gmail.com" == delete_user_data["username"]

    print(delete_user["message"])


async def get_account_info(access_token: str, test_client):
    authorization = f"bearer {access_token}"
    get_current_user = await test_client.get("/api/v1/account/info", headers={
        "Authorization": authorization
    })
    return get_current_user


async def get_refresh_token(signin_user) -> str:
    refresh_token = ''
    pattern = re.compile(r'refresh_token=([^;]+)')

    signin_user_headers = signin_user.__dict__["headers"].__dict__

    for header in signin_user_headers["_list"]:
        if "refresh_token" in header[2].decode('utf-8'):
            match = pattern.search(header[2].decode('utf-8'))
            if match:
                refresh_token = match.group(1)
                break
    return refresh_token
