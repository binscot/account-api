from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import api_router
from app.core import config, database
from app.exception.exception_handlers_setup import setup_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await database.mongo_client.connect()
        yield
        await database.mongo_client.disconnect()
    except Exception as e:
        raise e


def create_app() -> FastAPI:
    application = FastAPI(
        title="binscot-api",
        version="v1",
        lifespan=lifespan
    )

    application.include_router(api_router, prefix=config.settings.API_V1_STR)
    setup_exception_handlers(application)
    return application


app = create_app()
