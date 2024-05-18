from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi import Request
from fastapi.security.utils import get_authorization_scheme_param

from app.core.config import settings
from app.security.jwt.jwt_decoder import JWTDecoder
from app.security.jwt.jwt_encoder import JWTEncoder
from app.exception.exception_handlers_initializer import JwtError

JWT_SECRET_KEY = settings.JWT_SECRET_KEY
HASH_ALGORITHM = settings.HASH_ALGORITHM
TOKEN_TYPE = settings.TOKEN_TYPE
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_MINUTES = settings.REFRESH_TOKEN_EXPIRE_MINUTES


class JWTService:
    """
    create JWT access token
    create JWT refresh token
    check JWT token expired
    validate JWT token
    """

    def __init__(
            self,
            encoder: JWTEncoder,
            decoder: JWTDecoder,
            token_type: str = TOKEN_TYPE,
            algorithm: str = HASH_ALGORITHM,
            secret_key: str = JWT_SECRET_KEY,
            access_token_expire_time: int = ACCESS_TOKEN_EXPIRE_MINUTES,
            refresh_token_expire_time: int = REFRESH_TOKEN_EXPIRE_MINUTES

    ):
        self.encoder = encoder
        self.decoder = decoder
        self.token_type = token_type
        self.algorithm = algorithm
        self.secret_key = secret_key
        self.access_token_expire_time = access_token_expire_time
        self.refresh_token_expire_time = refresh_token_expire_time

    def create_access_token(self, data: dict) -> str:
        return self._create_token(data, self.access_token_expire_time)

    def create_refresh_token(self, data: dict) -> str:
        return self._create_token(data, self.refresh_token_expire_time)

    def _create_token(self, data: dict, expires_delta: int) -> str:
        return self.encoder.encode(data, expires_delta, self.secret_key, self.algorithm)

    def check_token_expired(self, token: str) -> dict | None:
        payload = self.decoder.decode(token, self.secret_key, self.algorithm)
        now = datetime.timestamp(datetime.now(ZoneInfo("Asia/Seoul")))
        if payload and payload["exp"] < now:
            return None

        return payload

    async def validate_token(self, request: Request) -> str | None:
        authorization = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != self.token_type:
            raise JwtError(info={"e": "Token is invalid", "scheme": scheme}, code=ErrorCode.BS108)
        return param


jwt_service = JWTService(JWTEncoder(), JWTDecoder())
