from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.log_analysis_schema import (
    LogAnalysisRequest,
    LogAnalysisResponse,
    LogAnalysisHistoryResponse,
    LogAnalysisResultResponse,
)
from app.services.log_analysis_service import analyze_log
from app.repositories.log_analysis_repository import (
    get_analysis_requests,
    get_analysis_request_by_id,
    get_analysis_result_by_request_id,
)

router = APIRouter(
    prefix="/api/logs",
    tags=["Log Analysis"]
)

# 로그 분석 요청 API
@router.post("/analyze", response_model=LogAnalysisResponse)
def analyze_log_api(
    request: LogAnalysisRequest,
    db: Session = Depends(get_db)
):
    return analyze_log(request, db)

# 분석 요청 이력을 조회
@router.get("", response_model=list[LogAnalysisHistoryResponse])
def get_analysis_requests_api(
    limit: int=20,
    offset: int=0,
    db: Session = Depends(get_db)
):
    return get_analysis_requests(db, limit=limit, offset=offset)

# 특정 분석 요청의 결과를 조회하는 API
@router.get("/{request_id}/result", response_model=LogAnalysisResultResponse)
def get_analysis_result_api(
    request_id: int,
    db: Session = Depends(get_db)
):
    # 사용자 요청 내역 확인 
    analysis_request = get_analysis_request_by_id(db, request_id)

    if analysis_request is None:
        raise HTTPException (
            status_code=404,
            detail="Log analysis request not found"
        )
    
    # LLM 답변 내역 확인
    analysis_result = get_analysis_result_by_request_id(db, request_id)

    if analysis_result is None:
        raise HTTPException(
            status_code=404,
            detail="Log analysis result not found"
        )

    return analysis_result