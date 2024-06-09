
from app.exceptions import exception_handlers_register, exception_handlers_initializer
from fastapi.exceptions import RequestValidationError


def setup_exception_handlers(app):
    app.add_exception_handler(
        exception_handlers_initializer.ValidationError,
        exception_handlers_register.validation_exception_handler
    )
    app.add_exception_handler(
        exception_handlers_initializer.InvalidPasswordError,
        exception_handlers_register.invalid_password_exception_handler
    )
    app.add_exception_handler(
        exception_handlers_initializer.DuplicateDataError,
        exception_handlers_register.duplicate_data_exception_handler
    )
    app.add_exception_handler(
        exception_handlers_initializer.RequiredDataError,
        exception_handlers_register.required_data_exception_handler
    )
    app.add_exception_handler(
        exception_handlers_initializer.NoApplicableDataError,
        exception_handlers_register.no_applicable_data_exception_handler
    )
    app.add_exception_handler(
        exception_handlers_initializer.CredentialsException,
        exception_handlers_register.credentials_exception_handler
    )
    app.add_exception_handler(
        exception_handlers_initializer.JwtError,
        exception_handlers_register.jwt_exception_handler
    )
    app.add_exception_handler(
        exception_handlers_initializer.PermissionDeniedError,
        exception_handlers_register.permission_denied_exception_handler
    )
    app.add_exception_handler(
        exception_handlers_initializer.TokenForgeryError,
        exception_handlers_register.token_forgery_exception_handler
    )
    app.add_exception_handler(
        exception_handlers_initializer.ExpiredTokenError,
        exception_handlers_register.expired_token_exception_handler
    )
    app.add_exception_handler(
        exception_handlers_initializer.InvalidTokenError,
        exception_handlers_register.invalid_token_exception_handler
    )
    app.add_exception_handler(
        RequestValidationError,
        exception_handlers_register.request_exception_handler
    )
