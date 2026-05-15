from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class DocumentCreateRequest(BaseModel):
    title: str = Field(..., example="결재 장애 대응 문서")
    document_type: str = Field(..., example="runbook")
    source: Optional[str] = Field(None, example="notion")    
    content: str = Field(
        ..., 
        example="결제 서비스에서 timeout이 발생하면 DB connection pool 상태를 확인한다."
    )

class DocumentCreateResponse(BaseModel):
    documentId: int
    title: str
    documentType: str
    source: Optional[str]
    chunkCount: int
    message: str
