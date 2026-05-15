from sqlalchemy.orm import Session

from app.models.document_chunk import DocumentChunk

class DocumentChunkRepository:
    def save_document_chunks(
        self,
        db: Session,
        chunk_data_list: list[dict]
    ) -> list[DocumentChunk]:
        chunks = []

        for chunk_data in chunk_data_list:
            chunk = DocumentChunk(
                document_id=chunk_data["document_id"],
                chunk_index=chunk_data["chunk_index"],
                content=chunk_data["content"],
                embedding=chunk_data["embedding"],
                token_count=chunk_data["token_count"],
                chunk_metadata=chunk_data["chunk_metadata"]
            )

            chunks.append(chunk)
        
        db.add_all(chunks)

        # for chunk in chunks:
        #     db.refresh(chunk)

        return chunks

    def get_chunks_by_document_id(
        self,
        db: Session,
        document_id: int
    ) -> list[DocumentChunk]:
        return (
            db.query(DocumentChunk)
            .filter(DocumentChunk.document_id == document_id)
            .order_by(DocumentChunk.chunk_index.asc())
            .all()
        )