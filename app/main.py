from fastapi import FastAPI

from app.api import auth
from app.core import config
from app.core import database
from app.exception.exception_handlers_setup import setup_exception_handlers

app = FastAPI()
app.include_router(auth.router, prefix=config.settings.API_V1_STR)
setup_exception_handlers(app)


@app.on_event("startup")
async def start_db():
    await database.mongodb.connect()
    await database.redis.connect()


@app.on_event("shutdown")
def shutdown_event():
    database.mongodb.close()
    database.redis.close()
