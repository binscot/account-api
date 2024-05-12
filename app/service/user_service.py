from beanie import PydanticObjectId
from passlib.context import CryptContext
from pydantic import EmailStr

from app.core import config
from app.enums.error_code import ErrorCode
from app.exception.exception_handlers_initializer import DataBaseError, ValidationError
from app.schemas.user_schema import User, UserShort, UserCreate

CRYPT_CONTEXT = config.settings.CRYPT_CONTEXT
password_context = CryptContext(schemes=[CRYPT_CONTEXT], deprecated="auto")


class UserService:
    @classmethod
    async def create_user(cls, req: UserCreate) -> UserShort | None:
        try:
            new_user = await User(
                username=req.username,
                join_type=req.join_type,
                service_type=req.service_type,
                hashed_password=password_context.hash(req.password1)
            ).create()
        except Exception as e:
            raise DataBaseError(info=e.__str__(), code=ErrorCode.BS102)
        db_user = await cls.get_user_short(new_user.username)
        return db_user

    @classmethod
    async def get_user(cls, username: str) -> User | None:
        try:
            user = await User.find_one(User.username == username)
        except Exception as e:
            raise DataBaseError(info=e.__str__(), code=ErrorCode.BS107)
        return user

    @classmethod
    async def get_user_short(cls, username: EmailStr) -> UserShort | None:
        try:
            user = await UserShort.find_one(UserShort.username == username)
        except Exception as e:
            raise DataBaseError(info=e.__str__(), code=ErrorCode.BS107)
        return user

    @classmethod
    async def get_user_short_by_id(cls, user_id: PydanticObjectId) -> UserShort | None:
        try:
            user = await UserShort.get(user_id)
        except Exception as e:
            raise DataBaseError(info=e.__str__(), code=ErrorCode.BS107)
        return user

    @classmethod
    def verify_password(cls, sign_password: str, hashed_password: str) -> bool:
        try:
            is_accurate = password_context.verify(sign_password, hashed_password)
        except Exception as e:
            raise ValidationError(info=e, code=ErrorCode.BS105)
        return is_accurate
