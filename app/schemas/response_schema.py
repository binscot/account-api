from typing import Any, Optional
from pydantic import BaseModel
from fastapi import Request


class CommonResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    data: Any = None
    request: Any = None


class ErrorResponse(BaseModel):
    error_code: Optional[str] = None
    success: bool
    message: Optional[str] = None
    request: Any

    @staticmethod
    def setting(request: Request, exc):
        return ErrorResponse(
            success=False,
            request={
                "client": request.client,
                "url": str(request.url),
                "body": exc.info
            }
        ).__dict__


class TokenResponse(BaseModel):
    access_token: Optional[str]
    username: Optional[str]
    id: Optional[str]
