from sqlalchemy.orm import Session

from app.models.log_analysis_request import LogAnalysisRequest

class LogAnalysisRequestRepository:
    #저장
    def save_analysis_request(
        self,
        db:Session,
        request_title: str | None,
        raw_log: str,
        service_name: str | None,
        environment: str | None,
        log_level: str | None,
        status: str = "PENDING"
    ) -> LogAnalysisRequest:
        
        analysis_request = LogAnalysisRequest(
            request_title=request_title,
            raw_log=raw_log,
            service_nam=service_name,
            environment=environment,
            log_level=log_level,
            status=status
        )

        db.add(analysis_request)
        db.commit()
        db.refresh(analysis_request)

        return analysis_request

    #상태변경
    def update_status(
        self,
        db:Session,
        request_id: int,
        status: str
    ) -> LogAnalysisRequest | None:
        analysis_request = (
            db.query(LogAnalysisRequest)
             .filter(LogAnalysisRequest.id == request_id)
             .first()
        )

        if analysis_request is None:
            return None
        
        analysis_request.status = status

        db.commit()
        db.refresh(analysis_request)

        return analysis_request
    
    #조회
    def find_by_id(
        self,
        db:Session,
        request_id: int
    ) -> LogAnalysisRequest | None:
        return (
            db.query(LogAnalysisRequest)
             .filter(LogAnalysisRequest.id == request_id)
             .first()
        )