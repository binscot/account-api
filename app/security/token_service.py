from fastapi import Response
from redis.asyncio import Redis

from app.schemas.response_schema import TokenResponse
from app.security.jwt.jwt_service import jwt_service


async def set_token_response(_id: str, response: Response, redis: Redis) -> TokenResponse:
    token_data = {"id": _id}
    access_token = jwt_service.create_access_token(token_data)
    refresh_token = jwt_service.create_refresh_token(token_data)
    """
       refresh_token redis 에 저장
       """
    redis_key = _id
    await redis.set(redis_key, refresh_token)
    response.set_cookie(key="access_token", value=access_token, httponly=True, secure=True)
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, secure=True)
    token_response = TokenResponse(
        access_token=access_token,
        username=None,
        id=_id
    )
    return token_response
