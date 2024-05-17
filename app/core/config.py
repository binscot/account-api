import os
from os import path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

base_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
load_dotenv()


class Settings(BaseSettings):
    API_V1_STR: str = "/api/account"

    CRYPT_CONTEXT: list[str] = os.getenv('CRYPT_CONTEXT')

    JWT_SECRET_KEY: str = os.getenv('JWT_SECRET_KEY')
    JWT_REFRESH_SECRET_KEY: str = os.getenv('JWT_REFRESH_SECRET_KEY')
    HASH_ALGORITHM: str = os.getenv('HASH_ALGORITHM')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')
    REFRESH_TOKEN_EXPIRE_MINUTES: int = os.getenv('REFRESH_TOKEN_EXPIRE_MINUTES')

    REDIS_SERVER: str = os.getenv('REDIS_SERVER')
    REDIS_PORT: str = os.getenv('REDIS_PORT')
    REDIS_PASSWORD: str = os.getenv('REDIS_PASSWORD')
    REDIS_DB: str = os.getenv('REDIS_DB')

    MONGO_SERVER: str = os.getenv('MONGO_SERVER')
    MONGO_PORT: str = os.getenv('MONGO_PORT')
    MONGO_PASSWORD: str = os.getenv('MONGO_PASSWORD')
    MONGO_ID: str = os.getenv('MONGO_ID')
    MONGO_DB_NAME: str = os.getenv('MONGO_DB_NAME')

    class Config:
        case_sensitive = True


settings = Settings()



