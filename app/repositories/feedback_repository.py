from sqlalchemy.orm import Session

from app.models.ai_feedback import AiFeedback

class FeedbackRepository:

    def save_feedback(
        self, 
        db:Session,
        result_id: int,
        feedback_type: str,
        comment: str | None
    ) -> AiFeedback:
        feedback = AiFeedback(
            result_id=result_id,
            feedback_type=feedback_type,
            comment=comment
        )
        db.add(feedback)
        db.commit()
        db.refresh(feedback)

        return feedback