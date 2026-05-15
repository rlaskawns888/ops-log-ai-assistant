from sqlalchemy.orm import Session

from app.schemas.log_analysis_schema import LogAnalysisRequest, LogAnalysisResponse
from app.repositories.log_analysis_repository import (
    save_analysis_request,
    save_analysis_result,
)

from app.services.vector_search_service import search_similar_chunks
from app.services.llm_service import generate_log_analysis

from app.utils.embedding import create_embedding


def analyze_log(
    request: LogAnalysisRequest,
    db: Session
) -> LogAnalysisResponse:
    saved_request = save_analysis_request(db, request) #요청 로그 저장

    query_embedding = create_embedding(request.raw_log) #Embedding

    similar_chunks = search_similar_chunks( #유사 로그 조회
        db=db,
        query_embedding=query_embedding,
        top_k=5
    )

    if not similar_chunks:
        saved_result = save_analysis_result( #결과 저장
            db=db,
            request_id=saved_request.id,
            summary="관련 운영 문서를 찾지 못했습니다.",
            root_cause="검색된 유사 운영 문서가 없어 원인을 특정할 수 없습니다.",
            recommended_action="운영 문서를 먼저 등록하거나 검색 기준을 개선한 뒤 다시 분석해주세요.",
            severity="UNKNOWN",
            model_name=None,
            prompt_version="v1",
            input_token_count=None,
            output_token_count=None
        )

        return LogAnalysisResponse(
            request_id=saved_request.id,
            summary=saved_result.summary,
            root_cause=saved_result.root_cause,
            recommended_action=saved_result.recommended_action,
            severity=saved_result.severity,
            referenced_chunks=[]
        )

    ai_result = generate_log_analysis(  #LLM API 호출
        log_message=request.raw_log,
        similar_chunks=similar_chunks
    )

    saved_result = save_analysis_result( #결과 저장
        db=db,
        request_id=saved_request.id,
        summary=ai_result["summary"],
        root_cause=ai_result["root_cause"],
        recommended_action=ai_result["recommended_action"],
        severity=ai_result["severity"],
        model_name=ai_result.get("model_name"),
        prompt_version=ai_result.get("prompt_version", "v1"),
        input_token_count=ai_result.get("input_token_count"),
        output_token_count=ai_result.get("output_token_count")
    )

    return LogAnalysisResponse(
        request_id=saved_request.id,
        summary=saved_result.summary,
        root_cause=saved_result.root_cause,
        recommended_action=saved_result.recommended_action,
        severity=saved_result.severity,
        referenced_chunks=similar_chunks
    )