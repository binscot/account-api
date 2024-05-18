from typing import Annotated

from fastapi import Depends, Request
from fastapi.security.utils import get_authorization_scheme_param

from app.exception.exception_handlers_initializer import JwtError
from app.security.jwt.jwt_service import jwt_service


async def validate_token(request: Request) -> str | None:
    authorization = request.headers.get("Authorization")
    scheme, param = get_authorization_scheme_param(authorization)
    if not authorization or scheme.lower() != "bearer":
        raise JwtError(info={"e": "Token is invalid", "scheme": scheme})
    return param


class JWTAuthentication:
    async def __call__(
            self,
            token: Annotated[str, Depends(validate_token)],
    ):
        try:
            valid_payload = jwt_service.check_token_expired(token)
            if valid_payload:
                return valid_payload.get("id")
            raise JwtError(info="Expired or changed token.")
        except Exception as e:
            raise JwtError(info={"e": e.__str__()})


GetCurrentUserByToken = JWTAuthentication()
