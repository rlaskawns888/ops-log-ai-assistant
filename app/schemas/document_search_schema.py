from pydantic import BaseModel, Field
from typing import List

class DocumentSearchRequest(BaseModel):
    query: str = Field(..., description="사용자 로그 또는 질문")
    top_k: int = Field(default=3, ge=1, le=10, description="검색 결과 개수")
    threshold: float = Field(default=0.35, description="검색 허용 distance 기준")

class DocumentSearchResult(BaseModel):
    documentId: int
    chunkId: int
    title: str
    source: str
    content: str
    distance: float

class DocumentSearchResponse(BaseModel):
    query: str
    top_k: int
    threshold: float
    results: List[DocumentSearchResult]
