from typing import Generic, Type, TypeVar, Union, Dict, Any

from beanie import PydanticObjectId
from fastapi.encoders import jsonable_encoder
from motor.core import AgnosticDatabase

from app.core.config import settings
from app.core.database import mongo_client
from app.schemas.user_schema import User, UserShort, UserCreate, UserUpdate

ModelType = TypeVar("ModelType", bound=[User, UserShort])
CreateSchemaType = TypeVar("CreateSchemaType", bound=[UserCreate])
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=[UserUpdate])


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model
        self.engine: mongo_client.mongo_client

    async def get(self, _id: PydanticObjectId) -> ModelType | None:
        # return await self.engine.find_one(self.model, self.model.id == id)
        return await self.model.find_one(self.model, self.model.id == _id)

    async def get_multi(self, *, page: int = 0, page_break: bool = False) -> list[
        ModelType]:  # noqa
        offset = {"skip": page * settings.MULTI_MAX, "limit": settings.MULTI_MAX} if page_break else {}  # noqa
        return await self.model.find(self.model, **offset)

    async def create(self, db: AgnosticDatabase, *, obj_in: CreateSchemaType) -> ModelType:  # noqa
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        return await self.model.save(db_obj)

    async def update(
            self, *, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]  # noqa
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        # TODO: Check if this saves changes with the setattr calls
        await self.model.save(db_obj)
        return db_obj

    async def remove(self, *, _id: PydanticObjectId) -> ModelType:
        obj = await self.model.get(id)
        if obj:
            await self.model.delete(obj)
        return obj
