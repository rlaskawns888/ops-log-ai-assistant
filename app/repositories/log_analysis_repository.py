from typing import Optional

from sqlalchemy.orm import Session

from app.models.log_analysis_request import LogAnalysisRequestModel
from app.models.log_analysis_result import LogAnalysisResultModel
from app.schemas.log_analysis_schema import LogAnalysisRequest

def save_analysis_request(
    db: Session,
    request: LogAnalysisRequest
) -> LogAnalysisRequestModel:
    analysis_request = LogAnalysisRequestModel(
        service_name=request.service_name,
        log_level=request.log_level,
        log_message=request.log_message
    )

    db.add(analysis_request)
    db.commit()
    db.refresh(analysis_request)

    return analysis_request


def save_analysis_result(
    db: Session,
    request_id: int,
    summary: str,
    cause: str,
    solution: str,
    confidence_score: float
) -> LogAnalysisResultModel:
    analysis_result = LogAnalysisResultModel(
        request_id=request_id,
        summary=summary,
        cause=cause,
        solution=solution,
        confidence_score=confidence_score
    )

    db.add(analysis_result)
    db.commit()
    db.refresh(analysis_result)

    return analysis_result

def get_analysis_request_by_id(
    db: Session,
    request_id: int
) -> Optional[LogAnalysisRequestModel]:
    return (
        db.query(LogAnalysisRequestModel)
         .filter(LogAnalysisRequestModel.id == request_id)
         .first()
    )

def get_analysis_result_by_request_id(
    db: Session,
    request_id: int
) -> Optional[LogAnalysisResultModel]:
    return (
        db.query(LogAnalysisResultModel)
         .filter(LogAnalysisResultModel.request_id == request_id)
         .first()
    )

def get_analysis_requests(
    db: Session,
    limit: int=20,
    offset: int=0
) -> list[LogAnalysisRequestModel]:
    return (
        db.query(LogAnalysisRequestModel)
         .order_by(LogAnalysisRequestModel.id.desc())
         .offset(offset)
         .limit(limit)
         .all()
    )