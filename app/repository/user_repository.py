from typing import Any, Dict, Union

from app.repository.base import BaseRepository
from app.schemas.user_schema import User
from app.schemas.user_schema import UserShort, UserCreate, UserUpdate
from app.security.password_service import password_service


class UserRepository(BaseRepository[User, UserShort, UserUpdate]):

    async def get_by_email(self, *, username: str) -> User | None:
        return await self.model.find_one(User.username == username)

    async def get_by_email_short(self, *, username: str) -> UserShort | None:
        return await self.model.find_one(UserShort.username == username)

    async def create(self, *, obj_in: UserCreate) -> User:
        return await super().create(obj_in=User(
            username=obj_in.username,
            hashed_password=password_service.get_password_hash(obj_in.password1),
            join_type=obj_in.join_type,
            service_type=obj_in.service_type
        ))

    async def update(self, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        if update_data.get("new_password"):
            hashed_password = password_service.get_password_hash(update_data["new_password"])
            del update_data["new_password"]
            del update_data["new_password_check"]
            update_data["hashed_password"] = hashed_password
        return await super().update(db_obj=db_obj, obj_in=update_data)


user = UserRepository(User)
user_short = UserRepository(UserShort)
