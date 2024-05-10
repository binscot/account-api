from datetime import datetime, timedelta
from typing import Annotated

from beanie import PydanticObjectId
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request
from fastapi import Response
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from app.core import config
from app.enums.error_code import ErrorCode
from app.enums.token_type import TokenType
from app.exception.exception_handlers_initializer import DataBaseError, JwtError
from app.models.model import User, UserShort
from app.schemas.response_schema import CommonResponse, ErrorResponse, TokenResponse
from app.schemas.user_schema import UserCreate
from app.core.database import redis

router = APIRouter()
CRYPT_CONTEXT = config.settings.CRYPT_CONTEXT
HASH_ALGORITHM = config.settings.HASH_ALGORITHM
password_context = CryptContext(schemes=[CRYPT_CONTEXT], deprecated="auto")


@router.post("/signup", response_model=CommonResponse | ErrorResponse)
async def signup(req: UserCreate):
    user = await get_user_short(req.username)
    if user:
        return CommonResponse(success=False, message=ErrorCode.BS101.message(), data=user.username, request=req.username)
    new_user = await create_user(req)
    return CommonResponse(success=True, message=None, data=new_user, request=new_user)


@router.post("/signin", response_model=CommonResponse | ErrorResponse)
async def signin(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], response: Response):

    user = await get_user(form_data.username)

    if not user:
        return CommonResponse(success=False, message=ErrorCode.BS103.message(), data=user, request=form_data.username)
    if not password_context.verify(form_data.password, user.hashed_password):
        return CommonResponse(success=False, message=ErrorCode.BS104.message(), data=None, request=form_data.username)

    refresh_token = create_jwt_token(data={"sub": str(user.id)}, token_type=TokenType.REFRESH_TOKEN)
    access_token = create_jwt_token(data={"sub": str(user.id)}, token_type=TokenType.ACCESS_TOKEN)
    token_response = TokenResponse(access_token=access_token, username=user.username, id=str(user.id))

    response.set_cookie(key=TokenType.REFRESH_TOKEN, value=refresh_token, httponly=True)

    response = CommonResponse(success=True, message=None, data=token_response, request=form_data.username)
    return response


@router.post("/token", response_model=CommonResponse | ErrorResponse)
async def create_access_token(request: Request):
    refresh_token = request.cookies.get(TokenType.REFRESH_TOKEN)
    if not refresh_token:
        return CommonResponse(success=False, message=ErrorCode.BS106.message(), data=None, request=None)

    user = await verify_token(refresh_token, TokenType.get_key(TokenType.REFRESH_TOKEN), HASH_ALGORITHM)
    access_token = create_jwt_token(data={"sub": str(user.id)}, token_type=TokenType.ACCESS_TOKEN)
    token_response = TokenResponse(access_token=access_token, username=user.username, id=str(user.id))

    return CommonResponse(success=True, message=None, data=token_response, request=None)


@router.post("/logout", response_model=CommonResponse | ErrorResponse)
async def logout(response: Response):
    try:
        response.delete_cookie(TokenType.REFRESH_TOKEN)
    except Exception as e:
        raise JwtError(info=e, code=ErrorCode.BS105)
    return CommonResponse(success=True, message=None, data=None, request=None)


@router.post("/redis_test", response_model=CommonResponse | ErrorResponse)
async def redis_test(key: str, value: str):
    redis.client.set(key, value)
    value = redis.client.get(key)
    return CommonResponse(
        success=True, message="redis test", data={
            "status_code": 200,
            "value": value
        }, request=None
    )


def create_jwt_token(data: dict, token_type: TokenType):
    expire = datetime.utcnow() + timedelta(minutes=TokenType.get_expire_minutes(token_type))
    try:
        to_encode = data.copy()
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, TokenType.get_key(token_type), algorithm=HASH_ALGORITHM)
    except Exception as e:
        raise JwtError(info={"e": e.__str__(), "token_type": token_type}, code=ErrorCode.BS105)
    return encoded_jwt


async def verify_token(token: str, secret_key: str, algorithm: str) -> UserShort:
    try:
        payload = jwt.decode(token, secret_key, algorithm)
        user_id = payload.get("sub")
    except Exception as e:
        raise JwtError(info={"e": e.__str__(), "token": token}, code=ErrorCode.BS108)
    return await get_user_short_by_id(user_id)


async def create_user(req: UserCreate) -> UserShort | None:
    try:
        new_user = await User(
            username=req.username,
            join_type=req.join_type,
            service_type=req.service_type,
            hashed_password=password_context.hash(req.password1)
        ).create()
    except Exception as e:
        raise DataBaseError(info=e.__str__(), code=ErrorCode.BS102)
    db_user = await get_user_short(new_user.username)
    return db_user


async def get_user_short_by_id(user_id: PydanticObjectId) -> UserShort | None:
    try:
        user = await UserShort.get(user_id)
    except Exception as e:
        raise DataBaseError(info=e.__str__(), code=ErrorCode.BS107)
    return user


async def get_user_short(username: EmailStr) -> UserShort | None:
    try:
        user = await UserShort.find_one(UserShort.username == username)
    except Exception as e:
        raise DataBaseError(info=e.__str__(), code=ErrorCode.BS107)
    return user


async def get_user(username: str) -> User | None:
    try:
        user = await User.find_one(User.username == username)
    except Exception as e:
        raise DataBaseError(info=e.__str__(), code=ErrorCode.BS107)
    return user
