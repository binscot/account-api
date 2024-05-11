from passlib.context import CryptContext

from app.core import config
from app.enums.error_code import ErrorCode
from app.exception.exception_handlers_initializer import ValidationError

CRYPT_CONTEXT = config.settings.CRYPT_CONTEXT
password_context = CryptContext(schemes=[CRYPT_CONTEXT], deprecated="auto")


def check_password(sign_password: str, hashed_password: str) -> bool:
    try:
        return password_context.verify(sign_password, hashed_password)
    except Exception as e:
        raise ValidationError(info=e, code=ErrorCode.BS105)

