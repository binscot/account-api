from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from jose import jwt


class AbstractJWTEncoder(ABC):
    """
    JWT encode
    @:param data: JWT에 담을 데이터
    @:param expires_delta: JWT 만료 시간
    @:param secret_key: JWT 암호화 키
    @:param algorithm: JWT 암호화 알고리즘
    """

    @abstractmethod
    def encode(
            self, data: dict, expires_delta: int, secret_key: str, algorithm: str
    ) -> str:
        pass


class JWTEncoder(AbstractJWTEncoder):
    def encode(
            self, data: dict, expires_delta: int, secret_key: str, algorithm: str
    ) -> str:
        to_encode = data.copy()
        expire = datetime.now(ZoneInfo("Asia/Seoul")) + timedelta(minutes=expires_delta)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, secret_key, algorithm=algorithm)



