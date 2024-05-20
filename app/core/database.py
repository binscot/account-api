from beanie import init_beanie
from motor import motor_asyncio

from app.core.config import settings
from app.schemas.user_schema import User, UserShort

MONGO_SERVER = settings.MONGO_SERVER
MONGO_PORT = settings.MONGO_PORT
MONGO_PASSWORD = settings.MONGO_PASSWORD
MONGO_ID = settings.MONGO_ID
MONGO_DB_NAME = settings.MONGO_DB_NAME
MONGO_SERVER_URL = settings.MONGO_SERVER_URL


class MongoDBClient:
    instance = None

    def __new__(cls):
        if not hasattr(cls, "instance") or cls.instance is None:
            cls.instance = super(MongoDBClient, cls).__new__(cls)
            cls.instance.mongo_client = motor_asyncio.AsyncIOMotorClient(
                f"mongodb://{MONGO_SERVER_URL}"
            )
            cls.instance.db = cls.instance.mongo_client[MONGO_DB_NAME]
        return cls.instance

    async def connect(self):
        try:
            await init_beanie(database=self.db, document_models=[User, UserShort])
            print("DB 와 연결되었습니다.")
        except Exception as e:
            print(f"MongoDB 연결 에러: {e}")

    async def disconnect(self):
        self.mongo_client.close()
        print("DB 연결 종료되었습니다.")

    async def get_collection(self, collection_name):
        return self.db[collection_name]


mongo_client = MongoDBClient()
