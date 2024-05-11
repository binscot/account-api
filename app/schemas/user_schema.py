from datetime import datetime
from typing import Optional

from beanie import Document
from pydantic import BaseModel, field_validator
from pydantic import EmailStr
from pydantic_core.core_schema import FieldValidationInfo

from app.enums.error_code import ErrorCode
from app.exception.exception_handlers_initializer import ValidationError


class User(Document):
    admin: bool = False
    username: EmailStr
    join_type: str
    service_type: str
    gender: Optional[str] = None
    birthday: Optional[str] = None
    phone_number: Optional[str] = None
    hashed_password: str
    disabled: bool = False
    created_at: datetime = datetime.utcnow()

    class Settings:
        name = "User"


class UserShort(Document):
    username: EmailStr
    created_at: datetime

    class Settings:
        name = "User"


class UserCreate(BaseModel):
    username: EmailStr
    join_type: Optional[str]
    service_type: Optional[str]
    password1: Optional[str]
    password2: Optional[str]

    @field_validator("*")
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValidationError(v, ErrorCode.BS111)
        return v

    @field_validator('password2')
    def passwords_match(cls, v, info: FieldValidationInfo):
        if 'password1' in info.data and v != info.data['password1']:
            raise ValidationError(v, ErrorCode.BS110)
        return v
