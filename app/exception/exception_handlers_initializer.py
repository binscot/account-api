from typing import Any


class CredentialsException(Exception):
    def __init__(self, info: Any):
        self.info = info


class ValidationError(Exception):
    def __init__(self, info: Any):
        self.info = info


class NotUniqueError(Exception):
    def __init__(self, info: Any):
        self.info = info


class DataBaseError(Exception):
    def __init__(self, info: Any):
        self.info = info


class JwtError(Exception):
    def __init__(self, info: Any):
        self.info = info


class RequestValidationError:
    pass
