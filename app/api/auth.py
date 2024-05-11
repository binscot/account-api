from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response, security

from app.core.database import redis
from app.crud import user_crud
from app.enums.error_code import ErrorCode
from app.enums.token_type import TokenType
from app.schemas.response_schema import CommonResponse, ErrorResponse, TokenResponse
from app.schemas.user_schema import UserCreate
from app.utils import common_util, token_util

router = APIRouter()


@router.post("/signup", response_model=CommonResponse | ErrorResponse)
async def signup(req: UserCreate):
    user = await user_crud.get_user_short(req.username)
    if user:
        return CommonResponse(success=False, message=ErrorCode.BS101.message(), data=user.username, request=req.username)
    new_user = await user_crud.create_user(req)
    return CommonResponse(success=True, message=None, data=new_user, request=new_user)


@router.post("/signin", response_model=CommonResponse | ErrorResponse)
async def signin(form_data: Annotated[security.OAuth2PasswordRequestForm, Depends()], response: Response):

    user = await user_crud.get_user(form_data.username)

    if not user:
        return CommonResponse(success=False, message=ErrorCode.BS103.message(), data=user, request=form_data.username)
    if not common_util.check_password(form_data.password, user.hashed_password):
        return CommonResponse(success=False, message=ErrorCode.BS104.message(), data=None, request=form_data.username)

    refresh_token = token_util.create_jwt_token(user.id, token_type=TokenType.REFRESH_TOKEN)
    access_token = token_util.create_jwt_token(user.id, token_type=TokenType.ACCESS_TOKEN)
    token_response = TokenResponse(access_token=access_token, username=user.username, id=str(user.id))

    # response.set_cookie(key=TokenType.REFRESH_TOKEN, value=refresh_token, httponly=True)
    await token_util.set_token_in_cookie(refresh_token, TokenType.REFRESH_TOKEN, response)
    response = CommonResponse(success=True, message=None, data=token_response, request=form_data.username)

    return response


@router.post("/token", response_model=CommonResponse | ErrorResponse)
async def create_access_token(request: Request):
    refresh_token = request.cookies.get(TokenType.REFRESH_TOKEN)
    if not refresh_token:
        return CommonResponse(success=False, message=ErrorCode.BS106.message(), data=None, request=None)

    user = await token_util.verify_token(refresh_token, TokenType.REFRESH_TOKEN)
    access_token = token_util.create_jwt_token(user.id, token_type=TokenType.ACCESS_TOKEN)
    token_response = TokenResponse(access_token=access_token, username=user.username, id=str(user.id))

    return CommonResponse(success=True, message=None, data=token_response, request=None)


@router.post("/logout", response_model=CommonResponse | ErrorResponse)
def logout(response: Response):
    is_sign_out = token_util.delete_jwt_token(response, TokenType.REFRESH_TOKEN)
    if not is_sign_out:
        return CommonResponse(success=False, message=None, data=None, request=None)
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



