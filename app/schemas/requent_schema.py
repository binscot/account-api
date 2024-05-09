from typing import Any, Optional
from pydantic import BaseModel


class CommonRequest(BaseModel):
    data: Any
    api_code: Optional[str]


class TestRequest(BaseModel):
    name: Optional[str]
    ida: Optional[int]
