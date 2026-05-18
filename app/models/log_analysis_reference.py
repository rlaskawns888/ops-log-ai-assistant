from sqlalchemy import Column, BigInteger, Integer, Float, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.core.database import Base

class LogAnalysisReference(Base):
    __tablename__ = "log_analysis_references"

    id = Column(BigInteger, primary_key=True, index=True)

    result_id = Column(
        BigInteger,
        ForeignKey("log_analysis.results.id", ondelete="CASCADE"),
        nullable=False
    )

    document_chunk_id = Column(
        BigInteger,
        ForeignKey("document_chunks.id", ondelete="CASCADE"),
        nullable=False
    )

    similarity_score = Column(Float, nullable=True)
    distance = Column(Float, nullable=True)
    rank_order = Column(Integer, nullable=False)

    created_at = Column(DateTime, nullable=False, server_default=func.now())
