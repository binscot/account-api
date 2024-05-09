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

    def error_response_setting(self: Request, exc):
        code = exc.__dict__.get('code')
        info = exc.__dict__.get('info')

        return ErrorResponse(
            error_code=code,
            success=False,
            message=ErrorCode.get_message(code),
            request={
                "client": self.client,
                "url": str(self.url),
                "body": info
            }
        ).__dict__
