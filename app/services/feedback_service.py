from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.feedback_repository import FeedbackRepository
from app.repositories.log_analysis_result_repository import LogAnalysisResultRepository
from app.schemas.feedback_schema import FeedbackCreateRequest

class FeedbackService:
    def __init__(self):
        self.feedback_repository = FeedbackRepository()
        self.log_analysis_result_repository = LogAnalysisResultRepository()

    
    def create_feedback(
        self,
        db: Session,
        request: FeedbackCreateRequest
    ):
        analysis_result = self.log_analysis_result_repository.find_by_id(
            db=db,
            result_id=request.result_id
        )

        if analysis_result is None:
            raise HTTPException(status_code=404, detail="Analysis result not found.")
        
        feedback = self.feedback_repository.save_feedback(
            db=db,
            result_id=analysis_result.id,
            feedback_type=request.feedback_type.value,
            comment=request.comment
        )

        return feedback