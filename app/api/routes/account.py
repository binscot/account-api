import json
import uuid
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, Response
from redis.asyncio import Redis

from app import repository
from app.api.dependencies import validate_user, get_current_user, get_redis_pool, get_current_user_short
from app.exception.exception_handlers_initializer import NotUniqueError, CredentialsException
from app.schemas.response_schema import CommonResponse, ErrorResponse, TokenResponse
from app.schemas.user_schema import UserCreate, User, UserUpdate, UserShort
from app.security.jwt.jwt_service import jwt_service
from app.service.password_service import password_service

router = APIRouter()


@router.post("/signup", response_model=CommonResponse | ErrorResponse)
async def register_user(req: UserCreate):
    user = await repository.user.get_by_email(username=req.username)
    if user:
        raise NotUniqueError(info="중복된 아이디")
    new_user = await repository.user.create(obj_in=req)
    return CommonResponse(
        success=True,
        message=None,
        data=new_user.username,
        request=new_user.username
    )


@router.post("/signin", response_model=CommonResponse | ErrorResponse)
async def perform_login(user: Annotated[UserShort, Depends(validate_user)], response: Response):
    """
    signin
    """
    token_data = {"id": str(user.id)}
    access_token = jwt_service.create_access_token(token_data)
    refresh_token = jwt_service.create_refresh_token(token_data)
    token_response = TokenResponse(
        access_token=access_token,
        username=user.username,
        id=str(user.id)
    )
    response.set_cookie(key="access_token", value=access_token, httponly=True, secure=True)
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, secure=True)
    response = CommonResponse(
        success=True,
        data=[token_response, user],
        request=None
    )
    return response


@router.get("/info", response_model=CommonResponse | ErrorResponse)
async def get_user_info(current_user: Annotated[UserShort, Depends(get_current_user_short)]):
    """
    get_user_me_short
    """
    return CommonResponse(success=True, data=current_user, request=current_user.username)


@router.get("/users", response_model=CommonResponse | ErrorResponse)
async def get_users():
    """
    get_users
    admin only
    """
    user_list = await repository.user_short.get_multi()
    return CommonResponse(success=True, data=user_list)


@router.put("/update", response_model=CommonResponse | ErrorResponse)
async def update_user(req: UserUpdate, current_user: Annotated[User, Depends(get_current_user)]):
    """
    Update user.
    """
    if req.original_password:
        if not password_service.verify_password(
                password=req.original_password,
                hashed_password=current_user.hashed_password
        ):
            raise CredentialsException(info="현재 비밀번호가 일치하지 않습니다.")
    await repository.user.update(db_obj=current_user, obj_in=req)
    update_user_short = await repository.user_short.get_by_email_short(username=current_user.username)
    return CommonResponse(success=True, data=update_user_short, message="update Successful")


@router.delete("/delete", response_model=CommonResponse | ErrorResponse)
async def delete_user(current_user: Annotated[User, Depends(get_current_user)]):
    """
    Delete user.
    """

    user = await repository.user_short.remove(_id=current_user.id)
    return CommonResponse(success=True, data=user, message="delete Successful")


@router.post("/token", response_model=CommonResponse | ErrorResponse)
async def get_access_token(user: Annotated[User, Depends(get_current_user)]):
    data = {"id": str(user.id)}
    access_token = jwt_service.create_access_token(data)
    token_response = TokenResponse(access_token=access_token, username=user.username, id=str(user.id))
    return CommonResponse(success=True, data=token_response)


@router.post("/logout", response_model=CommonResponse | ErrorResponse)
def logout(response: Response):
    response.delete_cookie("refresh_token")
    response.delete_cookie("access_token")
    return CommonResponse(success=True, message="logout Successful")


@router.post("/redis_test", response_model=CommonResponse | ErrorResponse)
async def redis_test(key: str, value: str, redis: Annotated[Redis, Depends(get_redis_pool)]):
    """
    Session 생성
    - 방장이 방을 생성한다.
    """
    session_id = str(f"{key}{uuid.uuid4()}")

    session_data = {
        "menu": [value],
        "expires_at": (datetime.now() + timedelta(minutes=10)).isoformat()
    }

    await redis.set(session_id, json.dumps(session_data), ex=600)
    result = await redis.get(session_id)
    result = json.loads(result)
    return CommonResponse(
        success=True, message="redis test", data={
            "key": session_id,
            "value": result
        }, request=None
    )
