from datetime import datetime
from typing import Optional

from beanie import Document
from pydantic import EmailStr


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
