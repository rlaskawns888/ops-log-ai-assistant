from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.feedback_schema import(
    FeedbackCreateRequest,
    FeedbackCreateResponse
)
from app.services.feedback_service import FeedbackService

router = APIRouter(
    prefix="/api/feedbacks",
    tags=["Feedbacks"]
)

feedback_service = FeedbackService()

# {
#   "resultId": 1,
#   "feedbackType": "HELPFUL",
#   "comment": "DB connection pool 확인 방향이 도움이 됐습니다."
# }
@router.post("", response_model=FeedbackCreateResponse)
def create_feedback(
    request: FeedbackCreateRequest,
    db: Session = Depends(get_db)
):
    feedback = feedback_service.create_feedback(
        db=db,
        request=request
    )

    return FeedbackCreateResponse(
        feedback_id=feedback.id,
        result_id=feedback.result_id,
        feedbackType=feedback.feedback_type,
        comment=feedback.comment,
        createdAt=feedback.created_at
    )