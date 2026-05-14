from sqlalchemy import Column, Integer, Text, Float, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.core.database import Base

#AI가 분석한 결과 저장
class LogAnalysisResultModel(Base):
    __tablename__ = "log_analysis_results"

    id = Column(Integer, primary_key=True, index=True)

    request_id = Column(
        Integer,
        ForeignKey("log_analysis_requests.id"),
        nullable=False
    )

    summary = Column(Text, nullable=False)
    cause = Column(Text, nullable=False)
    solution = Column(Text, nullable=False)
    confidence_score = Column(Float, nullable=False)

    create_at = Column(DateTime(timezone=True), server_default=func.now())