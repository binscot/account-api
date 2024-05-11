from typing import Any

from app.enums.error_code import ErrorCode


class CredentialsException(Exception):
    def __init__(self, info: Any, code=ErrorCode):
        self.info = info
        self.code = code


class ValidationError(Exception):
    def __init__(self, info: Any, code=ErrorCode):
        self.info = info
        self.code = code


class NotUniqueError(Exception):
    def __init__(self, info: Any, code=ErrorCode):
        self.info = info
        self.code = code


class DataBaseError(Exception):
    def __init__(self, info: Any, code=ErrorCode):
        self.info = info
        self.code = code


class JwtError(Exception):
    def __init__(self, info: Any, code=ErrorCode):
        self.info = info
        self.code = code


class RequestValidationError:
    pass
