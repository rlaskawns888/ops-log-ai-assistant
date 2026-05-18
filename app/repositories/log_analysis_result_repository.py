from sqlalchemy.orm import Session

from app.models.log_analysis_result import LogAnalysisResult


class LogAnalysisResultRepository:

    def save_result(
        self,
        db: Session,
        request_id: int,
        summary: str,
        root_cause: str | None,
        recommended_action: str | None,
        severity: str | None,
        model_name: str | None,
        prompt_version: str | None,
        input_token_count: int | None,
        output_token_count: int | None,
        total_tokens: int | None,
        latency_ms: int | None
    ) -> LogAnalysisResult:

        result = LogAnalysisResult(
            request_id=request_id,
            summary=summary,
            root_cause=root_cause,
            recommended_action=recommended_action,
            severity=severity,
            model_name=model_name,
            prompt_version=prompt_version,
            input_token_count=input_token_count,
            output_token_count=output_token_count,
            total_tokens=total_tokens,
            latency_ms=latency_ms
        )

        db.add(result)
        db.commit()
        db.refresh(result)

        return result

    def find_by_request_id(
        self,
        db: Session,
        request_id: int
    ) -> LogAnalysisResult | None:

        return (
            db.query(LogAnalysisResult)
            .filter(LogAnalysisResult.request_id == request_id)
            .first()
        )