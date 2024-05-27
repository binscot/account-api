"""User tests."""

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
    # Check that all the users attributes are returned + the generated ID, and that the status code is 201(created)
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

    assert "access_token" in signin_user_data
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
    access_token = signin_user_data["access_token"]
    authorization = f"bearer {access_token}"
    get_current_user = await test_client.get("/api/v1/account/info", headers={
        "Authorization": authorization
    })

    assert get_current_user.status_code == 200
    current_user = get_current_user.json()
    current_user_data = current_user["data"]
    assert "test@gmail.com" == current_user_data["username"]
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
    signin_user = signin_user.json()
    signin_user_data = signin_user["data"]
    access_token = signin_user_data["access_token"]
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
    access_token = signin_user_data["access_token"]
    authorization = f"bearer {access_token}"
    delete_user = await test_client.delete("/api/v1/account/delete", headers={
        "Authorization": authorization
    })
    assert delete_user.status_code == 200
    delete_user = delete_user.json()
    delete_user_data = delete_user["data"]
    assert "test@gmail.com" == delete_user_data["username"]
    print(delete_user["message"])
