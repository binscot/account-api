from datetime import datetime, timedelta

from beanie import PydanticObjectId
from fastapi import Response
from jose import jwt

from app.core import config
from app.enums.error_code import ErrorCode
from app.enums.token_type import TokenType
from app.exception.exception_handlers_initializer import JwtError
from app.schemas.user_schema import UserShort
from app.service.user_service import UserService

HASH_ALGORITHM = config.settings.HASH_ALGORITHM


def create_jwt_token(user_id: PydanticObjectId, token_type: TokenType):
    str_user_id = str(user_id)
    data = {"sub": str_user_id}
    expire = datetime.utcnow() + timedelta(minutes=TokenType.get_expire_minutes(token_type))
    try:
        to_encode = dict(data.copy())
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, TokenType.get_key(token_type), algorithm=HASH_ALGORITHM)
    except Exception as e:
        raise JwtError(info={"e": e.__str__(), "token_type": token_type}, code=ErrorCode.BS105)
    return encoded_jwt


def delete_jwt_token(response: Response, token_type: TokenType) -> bool:
    try:
        response.delete_cookie(token_type)
    except Exception as e:
        raise JwtError(info=e, code=ErrorCode.BS105)
    return True


async def verify_token(token: str, token_type: TokenType) -> UserShort:
    try:
        secret_key = TokenType.get_key(token_type)
        payload = jwt.decode(token, secret_key, HASH_ALGORITHM)
        user_id = payload.get("sub")
    except Exception as e:
        raise JwtError(info={"e": e.__str__(), "token": token}, code=ErrorCode.BS108)
    return await UserService.get_user_short_by_id(user_id)


async def set_token_in_cookie(token: str, token_type: TokenType, response: Response):
    try:
        response.set_cookie(key=token_type, value=token, httponly=True)
    except Exception as e:
        raise JwtError(info={"e": e.__str__(), "token": token}, code=ErrorCode.BS108)
    return response
