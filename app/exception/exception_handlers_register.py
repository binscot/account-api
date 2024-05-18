from fastapi import Request
from fastapi.responses import JSONResponse

from app.schemas.response_schema import ErrorResponse
from app.exception import exception_handlers_initializer


async def validation_exception_handler(
        request: Request,
        exc: exception_handlers_initializer.ValidationError
):
    return (
        JSONResponse(
            content=ErrorResponse.setting(request, exc),
            status_code=400)
    )


async def credentials_exception_handler(
        request: Request,
        exc: exception_handlers_initializer.CredentialsException
):
    return JSONResponse(
        content=ErrorResponse.setting(request, exc),
        status_code=400
    )


async def unique_exception_handler(
        request: Request,
        exc: exception_handlers_initializer.NotUniqueError
):
    return JSONResponse(
        content=ErrorResponse.setting(request, exc),
        status_code=400
    )


async def database_exception_handler(
        request: Request,
        exc: exception_handlers_initializer.DataBaseError
):
    return JSONResponse(
        content=ErrorResponse.setting(request, exc),
        status_code=500
    )


async def jwt_exception_handler(
        request: Request,
        exc: exception_handlers_initializer.JwtError
):
    return JSONResponse(
        content=ErrorResponse.setting(request, exc),
        status_code=500
    )


async def request_exception_handler(
        request: Request,
        exc: exception_handlers_initializer.RequestValidationError
):
    exc.info = exc.__str__()
    return JSONResponse(
        content=ErrorResponse.setting(request, exc),
        status_code=500
    )
