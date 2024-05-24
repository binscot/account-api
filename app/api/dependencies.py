from typing import Annotated

from fastapi import Depends, security
from redis import asyncio as aioredis

from app import repository
from app.core.config import settings
from app.exception.exception_handlers_initializer import JwtError, ValidationError
from app.schemas.user_schema import User, UserShort
from app.security.jwt.jwt_authentication import GetCurrentUserByToken
from app.service.password_service import password_service

REDIS_SERVER = settings.REDIS_SERVER
REDIS_PORT = settings.REDIS_PORT
REDIS_DB = settings.REDIS_DB
REDIS_PASSWORD = settings.REDIS_PASSWORD
REDIS_SERVER_URL = settings.REDIS_SERVER_URL


async def validate_user(form_data: Annotated[security.OAuth2PasswordRequestForm, Depends()]) -> User | None:
    db_user = await repository.user.get_by_email(username=form_data.username)
    if not db_user:
        raise ValidationError(info="해당 아이디를 가진 사용자가 존재하지 않습니다.")
    if not password_service.verify_password(password=form_data.password, hashed_password=db_user.hashed_password):
        raise ValidationError(info="비밀번호가 일치하지 않습니다.")
    return db_user


async def get_current_user(_id: Annotated[str, Depends(GetCurrentUserByToken)]) -> User | None:
    user = await repository.user.get(_id)
    if user is None:
        raise JwtError(info="Non-existent user")
    return user


async def get_current_user_short(_id: Annotated[str, Depends(GetCurrentUserByToken)]) -> UserShort | None:
    user = await repository.user_short.get(_id)
    if user is None:
        raise JwtError(info="Non-existent user")
    return user


async def is_admin(_id: Annotated[str, Depends(GetCurrentUserByToken)]) -> bool | None:
    user = await repository.user_short.get(_id)
    if user is None:
        raise JwtError(info="is not Admin User")
    if user.admin:
        return True
    return False


async def get_redis_pool():
    return await aioredis.from_url(f"redis://:{REDIS_SERVER_URL}")
