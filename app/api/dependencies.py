from typing import Annotated

from fastapi import Depends, security
from redis import asyncio as aioredis
from app import repository
from app.exception.exception_handlers_code import ErrorCode
from app.exception.exception_handlers_initializer import NotUniqueError, JwtError
from app.schemas.user_schema import User, UserShort
from app.security.jwt.jwt_authentication import GetCurrentUserByToken
from app.service.password_service import password_service
from app.core.config import settings

REDIS_SERVER = settings.REDIS_SERVER
REDIS_PORT = settings.REDIS_PORT
REDIS_DB = settings.REDIS_DB
REDIS_PASSWORD = settings.REDIS_PASSWORD


async def validate_user(form_data: Annotated[security.OAuth2PasswordRequestForm, Depends()]) -> User | None:
    db_user = await repository.user.get_by_email(username=form_data.username)
    if not db_user:
        raise NotUniqueError(info=ErrorCode.BS103.message(), code=ErrorCode.BS103)
    if not password_service.verify_password(password=form_data.password, hashed_password=db_user.hashed_password):
        raise NotUniqueError(info=ErrorCode.BS104.message(), code=ErrorCode.BS104)
    return db_user


async def get_current_user(_id: Annotated[str, Depends(GetCurrentUserByToken)]) -> User | None:
    user = await repository.user.get(_id)
    if user is None:
        raise JwtError(info={"e": "Non-existent user"}, code=ErrorCode.BS108)
    else:
        return user


async def get_current_user_short(_id: Annotated[str, Depends(GetCurrentUserByToken)]) -> UserShort | None:
    user = await repository.user_short.get(_id)
    if user is None:
        raise JwtError(info={"e": "Non-existent user"}, code=ErrorCode.BS108)
    else:
        return user


async def get_redis_pool():
    return await aioredis.from_url(f"redis://:{REDIS_PASSWORD}@{REDIS_SERVER}:{REDIS_PORT}/{REDIS_DB}")


