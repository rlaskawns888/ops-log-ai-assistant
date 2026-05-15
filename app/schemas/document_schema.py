from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class DocumentCreateRequest(BaseModel):
    title: str = Field(..., example="결재 장애 대응 문서")
    document_type: str = Field(..., example="runbook")
    source: Optional[str] = Field(None, example="notion")    
    content: str = Field(..., example="결제 서비스에서 timeout이 발생하면 DB connection pool 상태를 확인한다.")

class DocumentCreateResponse(BaseModel):
    document_id: int
    title: str
    document_type: str
    chunk_count: int

class DocumentResponse(BaseModel):
    id: int
    title: str
    document_type: str
    source: Optional[str] = None
    content: str
    created_at: datetime

    class Config:
        from_attributes = True