from sqlalchemy import Column, BigInteger, Integer, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from pgvector.sqlalchemy import Vector

from app.core.database import Base


#문서를 chunk로 쪼갠 뒤 embedding을 저장
class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(BigInteger, primary_key=True, index=True)

    document_id = Column(
        BigInteger, 
        ForeignKey("documents.id", ondelete="CASCADE"), 
        nullable=False
    )

    chunk_index = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)

    embedding = Column(Vector(1536), nullable=True)
    token_count = Column(Integer, nullable=True)

    # metadata = Column(JSONB, nullable=True)
    chunk_metadata = Column("metadata", JSONB, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    document = relationship(
        "Document",
        back_populates="chunks"
    )