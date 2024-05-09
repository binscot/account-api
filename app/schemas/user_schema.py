from typing import Optional

from pydantic import BaseModel, EmailStr, field_validator
from pydantic_core.core_schema import FieldValidationInfo
from beanie import PydanticObjectId
from datetime import datetime
from app.exception.exception_handlers_initializer import ValidationError


class UserBase(BaseModel):
    id: PydanticObjectId
    admin: bool
    username: EmailStr
    join_type: str
    service_type: str
    phone_number: Optional[str]
    gender: Optional[str]
    birthday: Optional[str]
    disabled: bool
    create_date: datetime


class UserInDB(UserBase):
    hashed_password: str

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    username: EmailStr
    join_type: Optional[str]
    service_type: Optional[str]
    password1: Optional[str]
    password2: Optional[str]

    @field_validator('username', 'password1', 'password2')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValidationError(v, '빈 값은 허용되지 않습니다.')
        return v

    @field_validator('password2')
    def passwords_match(cls, v, info: FieldValidationInfo):
        if 'password1' in info.data and v != info.data['password1']:
            raise ValidationError(v, 'passwords do not match')
        return v


class UserInfoRes(UserBase):
    pass
