from enum import StrEnum


class ErrorCode(StrEnum):
    ValidationError = "ValidationError"
    InvalidPasswordError = "InvalidPasswordError"
    DuplicateDataError = "DuplicateDataError"
    RequiredDataError = "RequiredDataError"
    NoApplicableDataError = "NoApplicableDataError"
    RequestValidationError = "RequestValidationError"
    CredentialsException = "CredentialsException"
    JwtError = "JwtError"
    PermissionDeniedError = "PermissionDeniedError"
    TokenForgeryError = "TokenForgeryError"
    ExpiredTokenError = "ExpiredTokenError"
    InvalidTokenError = "InvalidTokenError"

    def code(self):
        if self == "ValidationError":
            return "BS401"
        elif self == "InvalidPasswordError":
            return "BS402"
        elif self == "DuplicateDataError":
            return "BS404"
        elif self == "RequiredDataError":
            return "BS405"
        elif self == "NoApplicableDataError":
            return "BS406"
        elif self == "CredentialsException":
            return "BS407"
        elif self == "JwtError":
            return "BS408"
        elif self == "PermissionError":
            return "BS403"
        elif self == "TokenForgeryError":
            return "BS409"
        elif self == "ExpiredTokenError":
            return "BS410"
        elif self == "InvalidTokenError":
            return "BS411"
        elif self == "RequestValidationError":
            return "BS412"
