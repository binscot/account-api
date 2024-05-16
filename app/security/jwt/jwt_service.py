from datetime import datetime
from zoneinfo import ZoneInfo

from app.core.config import settings
from app.security.jwt.jwt_decoder import JWTDecoder
from app.security.jwt.jwt_encoder import JWTEncoder

JWT_SECRET_KEY = settings.JWT_SECRET_KEY
HASH_ALGORITHM = settings.HASH_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_MINUTES = settings.REFRESH_TOKEN_EXPIRE_MINUTES


class JWTService:
    """
    JWT 로그인시 access token, refresh token을 생성하는 로직
    """

    def __init__(
            self,
            encoder: JWTEncoder,
            decoder: JWTDecoder,
            algorithm: str = None,
            secret_key: str = JWT_SECRET_KEY,
            access_token_expire_time: int = ACCESS_TOKEN_EXPIRE_MINUTES,
            refresh_token_expire_time: int = REFRESH_TOKEN_EXPIRE_MINUTES,
    ):
        self.encoder = encoder
        self.decoder = decoder
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


jwt_service = JWTService(JWTEncoder(), JWTDecoder())
