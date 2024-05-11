from typing import Any, Optional
from pydantic import BaseModel
from fastapi import Request

from app.enums.error_code import ErrorCode


class CommonResponse(BaseModel):
    success: bool
    message: Optional[str]
    data: Any
    request: Any


class ErrorResponse(BaseModel):
    error_code: Optional[str]
    success: bool
    message: Optional[str]
    request: Any

    @staticmethod
    def setting(request: Request, exc):
        return ErrorResponse(
            error_code=exc.code,
            success=False,
            message=ErrorCode.message(exc.code),
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
