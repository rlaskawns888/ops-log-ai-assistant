from typing import Optional

from sqlalchemy.orm import Session

from app.models.log_analysis_request import LogAnalysisRequestModel
from app.models.log_analysis_result import LogAnalysisResultModel
from app.schemas.log_analysis_schema import LogAnalysisRequest


# 요청 로그 저장
def save_analysis_request(
    db: Session,
    request: LogAnalysisRequest
) -> LogAnalysisRequestModel:
    analysis_request = LogAnalysisRequestModel(
        request_title=request.request_title,
        raw_log=request.raw_log,
        service_name=request.service_name,
        environment=request.environment,
        log_level=request.log_level,
        status="PENDING"
    )

    db.add(analysis_request)
    db.commit()
    db.refresh(analysis_request)

    return analysis_request

#요청 결과 저장
def save_analysis_result(
    db: Session,
    request_id: int,
    summary: str,
    root_cause: str | None,
    recommended_action: str | None,
    severity: str | None,
    model_name: str | None = None,
    prompt_version: str | None = None,
    input_token_count: int | None = None,
    output_token_count: int | None = None
) -> LogAnalysisResultModel:
    analysis_result = LogAnalysisResultModel(
        request_id=request_id,
        summary=summary,
        root_cause=root_cause,
        recommended_action=recommended_action,
        severity=severity,
        model_name=model_name,
        prompt_version=prompt_version,
        input_token_count=input_token_count,
        output_token_count=output_token_count
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
    limit: int = 20,
    offset: int = 0
) -> list[LogAnalysisRequestModel]:
    return (
        db.query(LogAnalysisRequestModel)
        .order_by(LogAnalysisRequestModel.id.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )