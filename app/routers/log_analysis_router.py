from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.log_analysis_schema import (
    LogAnalysisRequest,
    LogAnalysisResponse,
    LogAnalysisHistoryResponse,
    LogAnalysisResultResponse,
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
#   "threshold": 0.35
# }

#로그 분석 API
@router.post(
    "/analyze",
    response_model=LogAnalysisResponse
)
def analyze_log(
    request: LogAnalysisRequest,
    db: Session = Depends(get_db)
):
    return log_analysis_service.analyze_log(
        request=request,
        db=db
    )


# #로그 분석 요청 이력 조회
# @router.get(
#     "/analysis-requests",
#     response_model=list[LogAnalysisHistoryResponse]
# )
# def get_analysis_requests(
#     limit: int = 20,
#     offset: int = 0,
#     db: Session = Depends(get_db)
# ):
#     return log_analysis_service.get_analysis_requests(
#         db=db,
#         limit=limit,
#         offset=offset
#     )

# #로그 분석 결과 상세 조회
# @router.get(
#     "/analysis-requests/{request_id}/result",
#     response_model=LogAnalysisResultResponse
# )
# def get_analysis_result(
#     request_id: int,
#     db: Session = Depends(get_db)
# ):
#     return log_analysis_service.get_analysis_result(
#         db=db,
#         request_id=request_id
#     )