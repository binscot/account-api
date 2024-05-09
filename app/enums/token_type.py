from enum import StrEnum

from app.core import config

JWT_SECRET_KEY = config.settings.JWT_SECRET_KEY
JWT_REFRESH_SECRET_KEY = config.settings.JWT_REFRESH_SECRET_KEY
ACCESS_TOKEN_EXPIRE_MINUTES = config.settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_MINUTES = config.settings.REFRESH_TOKEN_EXPIRE_MINUTES


class TokenType(StrEnum):
    ACCESS_TOKEN = "access_token"
    REFRESH_TOKEN = "refresh_token"

    def get_key(self):
        if self == "access_token":
            return JWT_SECRET_KEY
        elif self == "refresh_token":
            return JWT_REFRESH_SECRET_KEY

    def get_expire_minutes(self):
        if self == "access_token":
            return ACCESS_TOKEN_EXPIRE_MINUTES
        elif self == "refresh_token":
            return REFRESH_TOKEN_EXPIRE_MINUTES
