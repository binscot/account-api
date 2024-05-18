from typing import Generic, Type, TypeVar, Union, Dict, Any

from beanie import PydanticObjectId
from fastapi.encoders import jsonable_encoder

from app.core.config import settings
from app.core.database import mongo_client
from app.schemas.user_schema import User, UserShort, UserCreate, UserUpdate

ModelType = TypeVar("ModelType", bound=[User, UserShort])
CreateSchemaType = TypeVar("CreateSchemaType", bound=[UserCreate])
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=[UserUpdate])


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model
        self.engine: mongo_client.mongo_client

    async def get(self, _id: PydanticObjectId) -> ModelType | None:
        return await self.model.get(_id)

    async def get_multi(self, *, page: int = 0, page_break: bool = False) -> list[ModelType]:
        offset = {"skip": page * settings.MULTI_MAX, "limit": settings.MULTI_MAX} if page_break else {}

        cursor = self.model.find(**offset)
        return await cursor.to_list(length=None)

    async def create(self, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        return await self.model.save(db_obj)

    async def update(
            self, *, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        await self.model.save(db_obj)
        return db_obj

    async def remove(self, *, _id: PydanticObjectId) -> ModelType:
        obj = await self.model.get(_id)
        if obj:
            await self.model.delete(obj)
        return obj
