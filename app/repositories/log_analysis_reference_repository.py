from sqlalchemy.orm import Session

from app.models.log_analysis_reference import LogAnalysisReference
from app.models.document import Document
from app.models.document_chunk import DocumentChunk


class LogAnalysisReferenceRepository:

    def save_references(
        self,
        db: Session,
        result_id: int,
        similar_chunks: list[dict]
    ) -> list[LogAnalysisReference]:

        references = []

        for index, chunk in enumerate(similar_chunks):
            reference = LogAnalysisReference(
                result_id=result_id,
                document_chunk_id=chunk.get("chunk_id"),
                similarity_score=chunk.get("similarity_score"),
                distance=chunk.get("distance"),
                rank_order=index + 1
            )

            db.add(reference)
            references.append(reference)

        db.commit()

        for reference in references:
            db.refresh(reference)

        return references

    def find_by_result_id(
        self,
        db: Session,
        result_id: int
    ):
        return (
            db.query(
                DocumentChunk.id.label("chunk_id"),
                DocumentChunk.document_id.label("document_id"),
                Document.title.label("title"),
                DocumentChunk.content.label("content"),
                LogAnalysisReference.distance.label("distance"),
                LogAnalysisReference.similarity_score.label("similarity_score"),
                LogAnalysisReference.rank_order.label("rank_order"),
            )
            .join(
                DocumentChunk,
                LogAnalysisReference.document_chunk_id == DocumentChunk.id
            )
            .join(
                Document,
                DocumentChunk.document_id == Document.id
            )
            .filter(LogAnalysisReference.result_id == result_id)
            .order_by(LogAnalysisReference.rank_order.asc())
            .all()
        )