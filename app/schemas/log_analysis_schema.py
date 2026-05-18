from datetime import datetime
from typing import Optional, List, Literal

from pydantic import BaseModel, Field

#로그 분석 요청 Schema
class LogAnalysisRequest(BaseModel):
    request_title: Optional[str] = Field(
        default=None,
        description="로그 분석 요청 제목"
    )

    raw_log: str = Field(
        ...,
        description="분석할 원본 로그"
    )

    service_name: Optional[str] = Field(
        default=None,
        description="로그가 발생한 서비스 이름"
    )

    environment: Optional[str] = Field(
        default=None,
        description="실행 환경 예: prod, dev, stage"
    )

    log_level: Optional[str] = Field(
        default=None,
        description="로그 레벨 예: ERROR, WARN, INFO"
    )

    top_k: int = Field(
        default=3,
        description="유사 운영 문서 chunk 조회 개수"
    )

    threshold: float = Field(
        default=0.35,
        description="cosine distance 기준값. 값이 작을수록 더 유사함"
    )


#참조된 Chunk 응답 Schema
class SimilarChunkResponse(BaseModel):
    chunk_id: int
    document_id: int

    title: Optional[str] = Field(
        default=None,
        description="참조된 운영 문서 제목"
    )

    content: str

    distance: Optional[float] = Field(
        default=None,
        description="cosine distance 값. 작을수록 유사함"
    )

    similarity_score: Optional[float] = Field(
        default=None,
        description="유사도 점수. 필요 시 1 - distance 방식으로 계산 가능"
    )

    rank_order: Optional[int] = Field(
        default=None,
        description="검색 결과 순위"
    )


#로그 분석 API 응답 Schema
class LogAnalysisResponse(BaseModel):
    request_id: int

    result_id: Optional[int] = Field(
        default=None,
        description="저장된 AI 분석 결과 ID"
    )

    status: Literal[
        "ANALYZED",
        "INSUFFICIENT_CONTEXT"
    ]

    summary: Optional[str] = Field(
        default=None,
        description="로그 분석 요약"
    )

    root_cause: Optional[str] = Field(
        default=None,
        description="추정 원인"
    )

    recommended_action: Optional[str] = Field(
        default=None,
        description="권장 조치"
    )

    severity: Optional[str] = Field(
        default="UNKNOWN",
        description="장애 심각도 예: LOW, MEDIUM, HIGH, CRITICAL, UNKNOWN"
    )

    referenced_chunks: List[SimilarChunkResponse] = Field(
        default_factory=list,
        description="LLM 분석에 참조된 운영 문서 chunk 목록"
    )

    model_name: Optional[str] = Field(
        default=None,
        description="사용한 LLM 모델명"
    )

    prompt_version: Optional[str] = Field(
        default=None,
        description="프롬프트 버전"
    )

    input_token_count: Optional[int] = Field(
        default=None,
        description="LLM 요청 입력 토큰 수"
    )

    output_token_count: Optional[int] = Field(
        default=None,
        description="LLM 응답 출력 토큰 수"
    )

    total_tokens: Optional[int] = Field(
        default=None,
        description="LLM 요청/응답 전체 토큰 수"
    )

    latency_ms: Optional[int] = Field(
        default=None,
        description="AI 분석 처리 시간. 밀리초 단위"
    )

    message: Optional[str] = Field(
        default=None,
        description="분석 상태에 대한 추가 메시지"
    )


#로그 분석 요청 이력 응답 Schema
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


#로그 분석 결과 상세 응답 Schema
class LogAnalysisResultResponse(BaseModel):
    id: int
    request_id: int

    summary: Optional[str] = None
    root_cause: Optional[str] = None
    recommended_action: Optional[str] = None
    severity: Optional[str] = None

    model_name: Optional[str] = None
    prompt_version: Optional[str] = None

    input_token_count: Optional[int] = None
    output_token_count: Optional[int] = None

    total_tokens: Optional[int] = None
    latency_ms: Optional[int] = None

    created_at: datetime

    class Config:
        from_attributes = True

# 로그 분석 상세 조회 응답 Schema
class LogAnalysisDetailResponse(BaseModel):
    request: LogAnalysisHistoryResponse
    result: Optional[LogAnalysisResultResponse] = None
    referenced_chunks: List[SimilarChunkResponse] = Field(default_factory=list)