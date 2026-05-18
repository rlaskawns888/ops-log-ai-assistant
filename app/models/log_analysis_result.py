from sqlalchemy import Column, BigInteger, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.core.database import Base

#AI가 분석한 결과 저장
class LogAnalysisResult(Base):
    __tablename__ = "log_analysis_results"

    id = Column(BigInteger, primary_key=True, index=True)

    request_id = Column(
        BigInteger, 
        ForeignKey("log_analysis_requests.id"), 
        nullable=False,
        unique=True
    )

    summary = Column(Text, nullable=False)
    root_cause = Column(Text, nullable=True)
    recommended_action = Column(Text, nullable=True)
    severity = Column(String(20), nullable=True)

    model_name = Column(String(100), nullable=True)
    prompt_version = Column(String(50), nullable=True)

    input_token_count = Column(Integer, nullable=True)
    output_token_count = Column(Integer, nullable=True)
    total_tokens = Column(Integer, nullable=True)
    latency_ms = Column(Integer, nullable=True)

    created_at = Column(DateTime, server_default=func.now(), nullable=False)