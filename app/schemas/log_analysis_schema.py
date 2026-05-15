from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class LogAnalysisRequest(BaseModel):
    request_title: Optional[str] = Field(None, example="결제 서비스 DB Timeout 분석")
    raw_log: str = Field(
        ...,
        example="Database connection timeout occurred while processing payment request."
    )
    service_name: Optional[str] = Field(None, example="payment-service")
    environment: Optional[str] = Field(None, example="prod")
    log_level: Optional[str] = Field(None, example="ERROR")


class SimilarChunkResponse(BaseModel):
    chunk_id: int
    document_id: int
    content: str
    distance: Optional[float] = None
    similarity_score: Optional[float] = None
    rank_order: Optional[int] = None


class LogAnalysisResponse(BaseModel):
    request_id: int
    summary: str
    root_cause: Optional[str] = None
    recommended_action: Optional[str] = None
    severity: Optional[str] = None
    referenced_chunks: List[SimilarChunkResponse] = Field(default_factory=list)


class LogAnalysisHistoryResponse(BaseModel):
    id: int
    request_title: Optional[str] = None
    raw_log: str
    service_name: Optional[str] = None
    environment: Optional[str] = None
    log_level: Optional[str] = None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class LogAnalysisResultResponse(BaseModel):
    id: int
    request_id: int
    summary: str
    root_cause: Optional[str] = None
    recommended_action: Optional[str] = None
    severity: Optional[str] = None
    model_name: Optional[str] = None
    prompt_version: Optional[str] = None
    input_token_count: Optional[int] = None
    output_token_count: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True