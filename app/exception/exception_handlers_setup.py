from app.exception.exception_handlers_initializer import ValidationError, CredentialsException, NotUniqueError, \
    DataBaseError, JwtError
from app.exception import exception_handlers_register
from fastapi.exceptions import RequestValidationError


def setup_exception_handlers(app):
    app.add_exception_handler(
        ValidationError,
        exception_handlers_register.validation_exception_handler
    )
    app.add_exception_handler(
        CredentialsException,
        exception_handlers_register.credentials_exception_handler
    )
    app.add_exception_handler(
        NotUniqueError,
        exception_handlers_register.unique_exception_handler
    )
    app.add_exception_handler(
        DataBaseError,
        exception_handlers_register.database_exception_handler
    )
    app.add_exception_handler(
        JwtError,
        exception_handlers_register.jwt_exception_handler
    )
    app.add_exception_handler(
        RequestValidationError,
        exception_handlers_register.request_exception_handler
    )
