from typing import Annotated

from fastapi import Depends, Request
from fastapi import security
from fastapi.security.utils import get_authorization_scheme_param
from redis import asyncio as aioredis
from redis.asyncio import Redis

from app import repository
from app.core.config import settings
from app.exception.exception_handlers_initializer import JwtError
from app.exception.exception_handlers_initializer import ValidationError
from app.schemas.user_schema import User, UserShort
from app.security.jwt.jwt_service import jwt_service
from app.security.password_service import password_service

REDIS_SERVER = settings.REDIS_SERVER
REDIS_PORT = settings.REDIS_PORT
REDIS_DB = settings.REDIS_DB
REDIS_PASSWORD = settings.REDIS_PASSWORD
REDIS_SERVER_URL = settings.REDIS_SERVER_URL


async def get_redis_pool():
    return await aioredis.from_url(f"redis://{REDIS_SERVER_URL}")


async def validate_token(request: Request) -> str | None:
    authorization = request.headers.get("Authorization")
    scheme, param = get_authorization_scheme_param(authorization)
    if not authorization or scheme.lower() != "bearer":
        raise JwtError(info={"e": "Token is invalid", "scheme": scheme})
    return param


async def jwt_authentication(token: Annotated[str, Depends(validate_token)]) -> str | None:
    try:
        valid_payload = jwt_service.check_token_expired(token)
        if valid_payload:
            return valid_payload.get("id")
        raise JwtError(info="Expired or changed token.")
    except Exception as e:
        raise JwtError(info={"e": e.__str__()})


async def check_refresh_token(
        redis: Annotated[Redis, Depends(get_redis_pool)],
        _id: Annotated[str, Depends(jwt_authentication)],
        token: Annotated[str, Depends(validate_token)]
) -> bool | None:
    result = await redis.get(_id)
    return result.decode('utf-8') == token


async def validate_user(form_data: Annotated[security.OAuth2PasswordRequestForm, Depends()]) -> UserShort | None:
    db_user = await repository.user.get_by_email(username=form_data.username)
    if not db_user:
        raise ValidationError(info="해당 아이디를 가진 사용자가 존재하지 않습니다.")
    if not password_service.verify_password(password=form_data.password, hashed_password=db_user.hashed_password):
        raise ValidationError(info="비밀번호가 일치하지 않습니다.")
    return UserShort(
        id=db_user.id,
        admin=db_user.admin,
        username=db_user.username,
        created_at=db_user.created_at,
        join_type=db_user.join_type,
        service_type=db_user.service_type,
        gender=db_user.gender,
        birthday=db_user.birthday,
        phone_number=db_user.phone_number
    )


async def get_current_user(_id: Annotated[str, Depends(jwt_authentication)]) -> User | None:
    user = await repository.user.get(_id)
    if user is None:
        raise JwtError(info="Non-existent user")
    return user


async def get_current_user_short(_id: Annotated[str, Depends(jwt_authentication)]) -> UserShort | None:
    user = await repository.user_short.get(_id)
    if user is None:
        raise JwtError(info="Non-existent user")
    return user


async def is_admin(_id: Annotated[str, Depends(jwt_authentication)]) -> bool | None:
    user = await repository.user_short.get(_id)
    if user is None:
        raise JwtError(info="is not Admin User")
    if user.admin:
        return True
    return False
