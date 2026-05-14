from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func

from app.core.database import Base

#사용자가 로그 분석을 요청한 내용을 저장
class LogAnalysisRequestModel(Base):
    __tablename__ = "log_analysis_requests"

    id = Column(Integer, primary_key=True, index=True)

    service_name = Column(String(100), nullable=False)
    log_level = Column(String(20), nullable=False)
    log_message = Column(Text, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

