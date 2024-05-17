from typing import Annotated
from typing import Any, Dict, Union

from fastapi import Depends, security
from passlib.context import CryptContext

from app.core.config import settings
from app.enums.error_code import ErrorCode
from app.exception.exception_handlers_initializer import NotUniqueError
from app.repository.base import BaseRepository
from app.schemas.user_schema import User
from app.schemas.user_schema import UserShort, UserCreate, UserUpdate

password_context = CryptContext(schemes=settings.CRYPT_CONTEXT, deprecated="auto")


class UserRepository(BaseRepository[User, UserShort, UserUpdate]):

    async def get_by_email(self, *, username: str) -> User | None:
        return await self.model.find_one(User.username == username)

    async def get_by_email_short(self, *, username: str) -> UserShort | None:
        return await self.model.find_one(UserShort.username == username)

    async def create(self, *, obj_in: UserCreate) -> User:
        return await super().create(obj_in=User(
            username=obj_in.username,
            hashed_password=password_context.hash(obj_in.password1),
            join_type=obj_in.join_type,
            service_type=obj_in.service_type
        ))

    async def update(self, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        if update_data.get("new_password"):
            hashed_password = get_password_hash(update_data["new_password"])
            del update_data["new_password"]
            del update_data["new_password_check"]
            update_data["hashed_password"] = hashed_password
        return await super().update(db_obj=db_obj, obj_in=update_data)

    async def validate_user(self, form_data: Annotated[security.OAuth2PasswordRequestForm, Depends()]) -> User | None:
        db_user = await self.get_by_email(username=form_data.username)
        if not db_user:
            raise NotUniqueError(info=ErrorCode.BS103.message(), code=ErrorCode.BS103)
        if not verify_password(password=form_data.password, hashed_password=db_user.hashed_password):
            raise NotUniqueError(info=ErrorCode.BS104.message(), code=ErrorCode.BS104)
        return db_user


def verify_password(*, password: str, hashed_password: str) -> bool:
    return password_context.verify(password, hashed_password)


def get_password_hash(password: str) -> str:
    return password_context.hash(password)


user = UserRepository(User)
user_short = UserRepository(UserShort)
GetValidateUser = Annotated[User, Depends(user.validate_user)]
