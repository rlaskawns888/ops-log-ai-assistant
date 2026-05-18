from sqlalchemy.orm import Session

from app.models.log_analysis_reference import LogAnalysisReference


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
    ) -> list[LogAnalysisReference]:

        return (
            db.query(LogAnalysisReference)
            .filter(LogAnalysisReference.result_id == result_id)
            .order_by(LogAnalysisReference.rank_order.asc())
            .all()
        )