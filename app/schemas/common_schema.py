from pydantic import BaseModel
from typing import Optional

class ErrorResponse(BaseModel):
    message: str
    detail: Optional[str] = None

class HealthCheckResponse(BaseModel):
    status: str
    message: str