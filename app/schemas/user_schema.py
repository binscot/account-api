from datetime import datetime
from typing import Optional

from beanie import Document, Indexed
from pydantic import BaseModel, field_validator
from pydantic import EmailStr
from pydantic_core.core_schema import FieldValidationInfo

from app.exceptions.error_code import ErrorCode
from app.exceptions.exception_handlers_initializer import ValidationError, NoApplicableDataError, RequiredDataError, \
    InvalidPasswordError


class User(Document):
    admin: bool = False
    username: Indexed(EmailStr, unique=True)
    join_type: str
    service_type: str
    gender: Optional[str] = None
    birthday: Optional[str] = None
    phone_number: Optional[str] = None
    hashed_password: str
    disabled: bool = False
    created_at: datetime = datetime.utcnow()

    class Settings:
        name = "users"


class UserShort(Document):
    admin: bool
    username: EmailStr
    created_at: datetime
    join_type: str
    service_type: str
    gender: Optional[str] = None
    birthday: Optional[str] = None
    phone_number: Optional[str] = None

    class Settings:
        name = "users"


class UserCreate(BaseModel):
    username: EmailStr
    join_type: Optional[str]
    service_type: Optional[str]
    password1: Optional[str]
    password2: Optional[str]

    @field_validator("*")
    def not_empty(cls, v):
        if not v or not v.strip():
            raise RequiredDataError(
                error=ErrorCode.RequiredDataError,
                code=ErrorCode.RequiredDataError.code(),
                info="The data is not available."
            )
        return v

    @field_validator('password2')
    def passwords_match(cls, v, info: FieldValidationInfo):
        if 'password1' in info.data and v != info.data['password1']:
            raise InvalidPasswordError(
                error=ErrorCode.InvalidPasswordError,
                code=ErrorCode.InvalidPasswordError.code(),
                info="The password does not match."
            )
        return v


class UserUpdate(BaseModel):
    gender: Optional[str] = None
    birthday: Optional[str] = None
    phone_number: Optional[str] = None
    original_password: Optional[str] = None
    new_password: Optional[str] = None
    new_password_check: Optional[str] = None

    @field_validator("*")
    def not_empty(cls, v):
        if not v or not v.strip():
            raise RequiredDataError(
                error=ErrorCode.RequiredDataError,
                code=ErrorCode.RequiredDataError.code(),
                info="The data is not available."
            )
        return v

    @field_validator('new_password_check')
    def passwords_match(cls, v, info: FieldValidationInfo):
        if 'new_password' in info.data and v != info.data['new_password']:
            raise InvalidPasswordError(
                error=ErrorCode.InvalidPasswordError,
                code=ErrorCode.InvalidPasswordError.code(),
                info="The password does not match."
            )
        return v
