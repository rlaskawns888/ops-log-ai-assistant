from sqlalchemy.orm import Session

from app.schemas.log_analysis_schema import LogAnalysisRequest, LogAnalysisResponse
from app.repositories.log_analysis_repository import (
    save_analysis_request,
    save_analysis_result
)
from app.services.embedding_service import create_embedding
from app.services.vector_search_service import search_similar_chunks
from app.services.llm_service import generate_log_analysis

def analyze_log(
    request: LogAnalysisRequest,
    db: Session,    
) -> LogAnalysisResponse:
    saved_request = save_analysis_request(db, request) #사용자 로그 요청 저장 

    query_embedding = create_embedding(request.log_message) #embedding

    similar_chunks = search_similar_chunks( # 유사 chunk 조회
        db=db,
        query_embedding=query_embedding,
        top_k=5
    )

    if not similar_chunks:
        saved_result = save_analysis_result(
            db=db,
            request_id=saved_request.id,
            summary="관련 운영 문서를 찾지 못했습니다.",
            cause="검색된 유사 운영 문서가 없어 원인을 특정할 수 없습니다.",
            solution="운영 문서를 먼저 등록하거나 검색 기준을 개선한 뒤 다시 분석해주세요.",
            confidence_score=0.0
        )

        return LogAnalysisResponse(
            request_id=saved_request.id,
            summary=saved_result.summary,
            cause=saved_result.cause,
            solution=saved_result.solution,
            confidence_score=saved_result.confidence_score,
            referenced_chunks=[]
        )
    
    ai_result = generate_log_analysis( #LLM 분석 결과 반환
        log_message = request.log_message,
        similar_chunks = similar_chunks
    )

    saved_result = save_analysis_result( #DB저장 
        db=db,
        request_id=saved_request.id,
        summary=ai_result["summary"],
        cause=ai_result["cause"],
        solution=ai_result["solution"],
        confidence_score=ai_result["confidence_score"]
    )

    return LogAnalysisResponse(
        request_id=saved_request.id,
        summary=saved_result.summary,
        cause=saved_result.cause,
        solution=saved_result.solution,
        confidence_score=saved_result.confidence_score,
        referenced_chunks=similar_chunks
    )

