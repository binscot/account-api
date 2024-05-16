from typing import Annotated
from typing import Any, Dict, Union

from fastapi import Depends, security
from passlib.context import CryptContext

from app.core import config
from app.enums.error_code import ErrorCode
from app.exception.exception_handlers_initializer import NotUniqueError
from app.repository.base import CRUDBase
from app.schemas.user_schema import User
from app.schemas.user_schema import UserShort, UserCreate, UserUpdate

CRYPT_CONTEXT = config.settings.CRYPT_CONTEXT
# password_context = CryptContext(
#     schemes=["argon2", "bcrypt"], deprecated="auto"
#
# )
password_context = CryptContext(
    schemes=["bcrypt"], deprecated="auto")


class CRUDUser(CRUDBase[User, UserShort, UserUpdate]):

    async def get_by_email(self, *, username: str) -> User | None:  # noqa
        return await self.model.find_one(User.username == username)

    async def get_by_email(self, *, username: str) -> User | None:  # noqa
        return await self.model.find_one(User.username == username)

    async def get_by_email_short(self, *, username: str) -> UserShort | None:  # noqa
        return await self.model.find_one(UserShort.username == username)

    async def create(self, *, obj_in: UserCreate) -> User:  # noqa
        # TODO: Figure out what happens when you have a unique key like 'email'
        _user = {
            **obj_in.model_dump(),
            "username": obj_in.username,
            "hashed_password": password_context.hash(obj_in.password1),  # noqa
            "join_type": obj_in.join_type,
            "service_type": obj_in.service_type,
        }

        return await self.model.save(User(**_user))

    async def update(self, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]) -> User:  # noqa
        print(db_obj)
        print(obj_in)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        print("============")
        print(update_data)
        if update_data.get("original_password"):
            hashed_password = get_password_hash(update_data["original_password"])
            del update_data["original_password"]
            update_data["hashed_password"] = hashed_password
        print(update_data)
        return await super().update(db_obj=db_obj, obj_in=update_data)

    async def authenticate(self, *, username: str, password: str) -> User | None:  # noqa
        db_user = await self.get_by_email(username=username)
        if not db_user:
            return None
        if not verify_password(plain_password=password, hashed_password=db_user.hashed_password):  # noqa
            return None
        return db_user

    async def validate_user(self, form_data: Annotated[security.OAuth2PasswordRequestForm, Depends()]) -> User | None:
        db_user = await self.get_by_email(username=form_data.username)
        if not db_user:
            raise NotUniqueError(info=ErrorCode.BS103.message(), code=ErrorCode.BS103)
        if not self.authenticate(username=form_data.username, password=form_data.password):
            raise NotUniqueError(info=ErrorCode.BS104.message(), code=ErrorCode.BS104)
        return db_user


def verify_password(*, plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return password_context.hash(password)


GetValidateUser = Annotated[User, Depends(CRUDUser(User).validate_user)]
user = CRUDUser(User)
user_short = CRUDUser(UserShort)
