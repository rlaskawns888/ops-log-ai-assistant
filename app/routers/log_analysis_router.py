from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.log_analysis_schema import (
    LogAnalysisRequest,
    LogAnalysisResponse,
    LogAnalysisHistoryResponse,
    LogAnalysisResultResponse,
    LogAnalysisDetailResponse,
)
from app.services.log_analysis_service import LogAnalysisService


router = APIRouter(
    prefix="/api/logs",
    tags=["Log Analysis"]
)

log_analysis_service = LogAnalysisService()


# {
#   "request_title": "결제 서비스 DB Timeout 분석",
#   "raw_log": "Database connection timeout occurred while processing payment request.",
#   "service_name": "payment-service",
#   "environment": "prod",
#   "log_level": "ERROR",
#   "top_k": 3,
#   "threshold": 1.0
# }
#로그 분석 API
@router.post(
    "/analyze",
    response_model=LogAnalysisResponse
)
async def analyze_log(
    request: LogAnalysisRequest,
    db: Session = Depends(get_db)
):
    return await log_analysis_service.analyze_log(
        request=request,
        db=db
    )

# 로그 분석 상세 조회 API
@router.get("/{analysis_id}", response_model=LogAnalysisDetailResponse)
def get_log_analysis_detail(
    analysis_id: int,
    db: Session = Depends(get_db)
):
    return log_analysis_service.get_analysis_detail(
        analysis_id=analysis_id,
        db=db
    )