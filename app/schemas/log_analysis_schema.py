from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

#사용자가 로그 분석을 요청
class LogAnalysisRequest(BaseModel):
    service_name: str = Field(..., example="payment-service")
    log_level: str = Field(..., example="ERROR") #ERROR, WARN, INFO 같은 로그 레벨
    log_message: str = Field(
        ...,
        example="Database connection timeout occurred while processing payment request."
    )

class SimilarChunkResponse(BaseModel):
    chunk_id: int
    document_id: int
    content: str
    distance: Optional[float] = None

#AI 분석 결과
class LogAnalysisResponse(BaseModel):
    request_id: int
    summary: str
    cause: str
    solution: str
    confidence_score: float
    referenced_chunks: List[SimilarChunkResponse] = []

class LogAnalysisHistoryResponse(BaseModel):
    id: int
    service_name: str
    log_level: str
    log_message: str
    create_at: datetime

    class Config:
        from_attributes = True

class LogAnalysisResultResponse(BaseModel):
    id: int
    request_id: int
    summary: str
    cause: str
    solution: str
    confidence_score: float
    create_at: datetime

    class Config:
        from_attributes = True