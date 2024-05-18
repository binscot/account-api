import json
import uuid
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, Response
from redis import asyncio as aioredis

from app import repository
from app.api.dependencies import validate_user, get_current_user, get_redis_pool, get_current_user_short
from app.exception.exception_handlers_code import ErrorCode
from app.exception.exception_handlers_initializer import NotUniqueError
from app.schemas.response_schema import CommonResponse, ErrorResponse, TokenResponse
from app.schemas.user_schema import UserCreate, User, UserUpdate, UserShort
from app.security.jwt.jwt_service import jwt_service
from app.service.password_service import password_service

router = APIRouter()


@router.post("/signup", response_model=CommonResponse | ErrorResponse)
async def signup(req: UserCreate):
    user = await repository.user.get_by_email(username=req.username)
    if user:
        raise NotUniqueError(info=ErrorCode.BS101.message(), code=ErrorCode.BS101)
    new_user = await repository.user.create(obj_in=req)
    return CommonResponse(
        success=True,
        message=None,
        data=new_user.username,
        request=new_user.username
    )


@router.post("/signin", response_model=CommonResponse | ErrorResponse)
async def signin(user: Annotated[User, Depends(validate_user)], response: Response):
    """
    signin

    """
    data = {"id": str(user.id)}
    access_token = jwt_service.create_access_token(data)
    refresh_token = jwt_service.create_refresh_token(data)
    token_response = TokenResponse(access_token=access_token, username=user.username, id=str(user.id))
    response.set_cookie(key="access_token", value=access_token, httponly=True, secure=True)
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, secure=True)
    response = CommonResponse(success=True, data=token_response, request=user.username)
    return response


@router.get("/me", response_model=CommonResponse | ErrorResponse)
async def get_user_me(current_user: Annotated[UserShort, Depends(get_current_user_short)]):
    """
    get_user_me_short
    """
    return CommonResponse(success=True, data=current_user, request=current_user.username)


@router.get("/users", response_model=CommonResponse | ErrorResponse)
async def get_users():
    """
    get_user_me_short
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
            raise NotUniqueError(info="비밀번호가 일치하지 블라블라", code=ErrorCode.BS101)
    user = await repository.user.update(db_obj=current_user, obj_in=req)
    return CommonResponse(success=True, message=user.username)


@router.post("/token", response_model=CommonResponse | ErrorResponse)
async def token_check(user: Annotated[User, Depends(get_current_user)]):
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
async def redis_test(key: str, value: str, redis: Annotated[aioredis.Redis, Depends(get_redis_pool)]):
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
