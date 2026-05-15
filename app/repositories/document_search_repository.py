from sqlalchemy.orm import Session
from sqlalchemy import asc

from app.models.document import Document
from app.models.document_chunk import DocumentChunk

class DocumentSearchRepository:

    # top_k: 유사도가 높은 chunk를 최대 몇 개까지 가져올지 제한
    # distance(거리): query embedding과 chunk embedding 사이의 거리
    # distance가 낮을수록 더 유사한 문서 chunk
    # threshold: distance가 이 값 이하인 chunk만 검색 결과로 인정
    def search_similar_chunks(
        self,
        db: Session,
        query_embedding: list[float],
        top_k: int,
        threshold: float
    ): 
        distance = DocumentChunk.embedding.cosine_distance(query_embedding)         
        # ORM에서 아래의 쿼리로 변환됨
        # ex) document_chunks.embedding <=> query_embedding

        rows = (
            db.query(
                DocumentChunk.id.label("chunk_id"),
                DocumentChunk.document_id.label("document_id"),
                Document.title.label("title"),
                Document.source.label("source"),
                DocumentChunk.content.label("content"),
                distance.label("distance"),
            )
            .join(Document, Document.id == DocumentChunk.document_id)
            .filter(distance <= threshold)
            .order_by(asc(distance))
            .limit(top_k)
            .all()
        )

        return rows


