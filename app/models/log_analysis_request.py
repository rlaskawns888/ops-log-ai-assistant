from sqlalchemy import Column, BigInteger, String, Text, DateTime
from sqlalchemy.sql import func

from app.core.database import Base

#사용자가 로그 분석을 요청한 내용을 저장
class LogAnalysisRequest(Base):
    __tablename__ = "log_analysis_requests"

    id = Column(BigInteger, primary_key=True, index=True)

    request_title = Column(String(255), nullable=True)
    raw_log = Column(Text, nullable=False)

    service_name = Column(String(100), nullable=True)
    environment = Column(String(50), nullable=True)
    log_level = Column(String(20), nullable=True)
    
    status = Column(String(30), nullable=False, default="PENDING")

    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

