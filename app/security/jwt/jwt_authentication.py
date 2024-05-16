from fastapi import Depends, Request
from fastapi.security.utils import get_authorization_scheme_param
from typing import Annotated
from app.security.jwt.jwt_service import jwt_service
from app.enums.error_code import ErrorCode
from app.exception.exception_handlers_initializer import JwtError
from app.repository import user_repository
from app.schemas.user_schema import User


async def validate_token(request: Request) -> str | None:
    authorization = request.headers.get("Authorization")
    scheme, param = get_authorization_scheme_param(authorization)
    if not authorization or scheme.lower() != "bearer":
        raise JwtError(info={"e": "Token is invalid", "scheme": scheme}, code=ErrorCode.BS108)
    return param


class JWTAuthentication:
    async def __call__(
            self,
            token: Annotated[str, Depends(validate_token)],
    ):
        try:
            valid_payload = jwt_service.check_token_expired(token)
            if valid_payload:
                _id = valid_payload.get("id")
            else:
                raise JwtError(info={"e": "Expired or changed token."}, code=ErrorCode.BS108)
        except Exception as e:
            raise JwtError(info={"e": e.__str__()}, code=ErrorCode.BS108)
        else:
            user = await user_repository.user.get(_id)
            if user is None:
                raise JwtError(info={"e": "Non-existent user"}, code=ErrorCode.BS108)
            else:
                return user


get_current_user = JWTAuthentication()
GetCurrentUser = Annotated[User, Depends(get_current_user)]
