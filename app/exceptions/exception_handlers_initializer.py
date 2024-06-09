from enum import StrEnum


class BSBaseException(Exception):
    def __init__(self, error: StrEnum, code: str, info: str):
        self.error = error
        self.code = code
        self.info = info


class ValidationError(BSBaseException):
    def __init__(self, error: StrEnum, code: str, info: str):
        super().__init__(error, code, info)


class InvalidPasswordError(BSBaseException):
    def __init__(self, error: StrEnum, code: str, info: str):
        super().__init__(error, code, info)


class DuplicateDataError(BSBaseException):
    def __init__(self, error: StrEnum, code: str, info: str):
        super().__init__(error, code, info)


class RequiredDataError(BSBaseException):
    def __init__(self, error: StrEnum, code: str, info: str):
        super().__init__(error, code, info)


class NoApplicableDataError(BSBaseException):
    def __init__(self, error: StrEnum, code: str, info: str):
        super().__init__(error, code, info)


class CredentialsException(BSBaseException):
    def __init__(self, error: StrEnum, code: str, info: str):
        super().__init__(error, code, info)


class JwtError(BSBaseException):
    def __init__(self, error: StrEnum, code: str, info: str):
        super().__init__(error, code, info)


class PermissionDeniedError(BSBaseException):
    def __init__(self, error: StrEnum, code: str, info: str):
        super().__init__(error, code, info)


class TokenForgeryError(BSBaseException):
    def __init__(self, error: StrEnum, code: str, info: str):
        super().__init__(error, code, info)


class ExpiredTokenError(BSBaseException):
    def __init__(self, error: StrEnum, code: str, info: str):
        super().__init__(error, code, info)


class InvalidTokenError(BSBaseException):
    def __init__(self, error: StrEnum, code: str, info: str):
        super().__init__(error, code, info)


class RequestValidationError:
    pass
