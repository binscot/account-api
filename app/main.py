from contextlib import asynccontextmanager

from fastapi import FastAPI
import socket
from app.api.router import api_router
from app.core import config, database
from app.core.logging import logger
from app.exceptions.exception_handlers_setup import setup_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    host = socket.gethostname()
    ip_addr = socket.gethostbyname(host)
    logger.info(f"host :{host}")
    logger.info(f"ip_addr :{ip_addr}")
    await database.mongo_client.connect()
    yield
    await database.mongo_client.disconnect()


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
