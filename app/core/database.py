import motor.motor_asyncio
from beanie import init_beanie
from redis.client import Redis

from app.core.config import settings
from app.schemas.user_schema import User, UserShort

REDIS_SERVER = settings.REDIS_SERVER
REDIS_PORT = settings.REDIS_PORT
REDIS_DB = settings.REDIS_DB
REDIS_PASSWORD = settings.REDIS_PASSWORD

MONGO_SERVER = settings.MONGO_SERVER
MONGO_PORT = settings.MONGO_PORT
MONGO_PASSWORD = settings.MONGO_PASSWORD
MONGO_ID = settings.MONGO_ID
MONGO_DB_NAME = settings.MONGO_DB_NAME


class MongoDB:
    def __init__(self):
        self.client = None
        self.database = None

    async def connect(self):
        try:

            self.client = motor.motor_asyncio.AsyncIOMotorClient(
                f"mongodb://{MONGO_ID}:{MONGO_PASSWORD}@{MONGO_SERVER}:{MONGO_PORT}"
            )
            self.database = self.client[MONGO_DB_NAME]

            await init_beanie(database=self.database, document_models=[User, UserShort])
            print("DB 와 연결되었습니다.")
        except Exception as e:
            print(f"MongoDB 연결 에러: {e}")

    def close(self):
        self.client.close()
        print("DB 연결 종료되었습니다.")


mongodb = MongoDB()


class RedisDB:
    def __init__(self):
        self.client = None

    async def connect(self):
        try:
            self.client = Redis(host=REDIS_SERVER, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD)
            print("redis 와 연결되었습니다.")
        except Exception as e:
            print(f"redis 연결 에러: {e}")

    def close(self):
        self.client.close()
        print("redis 연결 종료되었습니다.")


redis = RedisDB()
