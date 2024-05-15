from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import auth
from app.core import config, database
from app.exception.exception_handlers_setup import setup_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        print("application start")
        await database.mongo_client.connect()
        await database.redis_client.connect()
        yield
        await database.mongo_client.disconnect()
        database.redis_client.close()
        print("application end")

    except Exception as e:
        raise e


app = FastAPI(lifespan=lifespan)
app.include_router(auth.router, prefix=config.settings.API_V1_STR)
setup_exception_handlers(app)
