from fastapi import Request
from fastapi.responses import JSONResponse

from app.exceptions.error_code import ErrorCode
from app.schemas.response_schema import ErrorResponse
from app.exceptions import exception_handlers_initializer


async def validation_exception_handler(
        request: Request,
        exc: exception_handlers_initializer.ValidationError
):
    return (
        JSONResponse(
            content=ErrorResponse.setting(request, exc),
            status_code=400)
    )


async def invalid_password_exception_handler(
        request: Request,
        exc: exception_handlers_initializer.InvalidPasswordError
):
    return (
        JSONResponse(
            content=ErrorResponse.setting(request, exc),
            status_code=400)
    )


async def duplicate_data_exception_handler(
        request: Request,
        exc: exception_handlers_initializer.DuplicateDataError
):
    return JSONResponse(
        content=ErrorResponse.setting(request, exc),
        status_code=400
    )


async def required_data_exception_handler(
        request: Request,
        exc: exception_handlers_initializer.RequiredDataError
):
    return JSONResponse(
        content=ErrorResponse.setting(request, exc),
        status_code=400
    )


async def no_applicable_data_exception_handler(
        request: Request,
        exc: exception_handlers_initializer.NoApplicableDataError
):
    return JSONResponse(
        content=ErrorResponse.setting(request, exc),
        status_code=400
    )


async def credentials_exception_handler(
        request: Request,
        exc: exception_handlers_initializer.CredentialsException
):
    return JSONResponse(
        content=ErrorResponse.setting(request, exc),
        status_code=401
    )


async def jwt_exception_handler(
        request: Request,
        exc: exception_handlers_initializer.JwtError
):
    return JSONResponse(
        content=ErrorResponse.setting(request, exc),
        status_code=401
    )


async def permission_denied_exception_handler(
        request: Request,
        exc: exception_handlers_initializer.PermissionDeniedError
):
    return JSONResponse(
        content=ErrorResponse.setting(request, exc),
        status_code=403
    )


async def token_forgery_exception_handler(
        request: Request,
        exc: exception_handlers_initializer.TokenForgeryError
):
    return JSONResponse(
        content=ErrorResponse.setting(request, exc),
        status_code=401
    )


async def expired_token_exception_handler(
        request: Request,
        exc: exception_handlers_initializer.ExpiredTokenError
):
    return JSONResponse(
        content=ErrorResponse.setting(request, exc),
        status_code=401
    )


async def invalid_token_exception_handler(
        request: Request,
        exc: exception_handlers_initializer.InvalidTokenError
):
    return JSONResponse(
        content=ErrorResponse.setting(request, exc),
        status_code=401
    )


async def request_exception_handler(
        request: Request,
        exc: exception_handlers_initializer.RequestValidationError
):
    exc.error = ErrorCode.RequestValidationError
    exc.code = ErrorCode.RequestValidationError.code()
    exc.info = exc.__str__()
    return JSONResponse(
        content=ErrorResponse.setting(request, exc),
        status_code=400
    )
