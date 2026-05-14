from sqlalchemy.orm import Session

from app.models.document_chunk import DocumentChunkModel

def save_document_chunks(
    db: Session,
    chunk_data_list: list[dict]
) -> list[DocumentChunkModel]:
    chunks = []

    for chunk_data in chunk_data_list:
        chunk = DocumentChunkModel(
            document_id = chunk_data["document_id"],
            chunk_index = chunk_data["chunk_index"],
            content=chunk_data["content"],
            embedding=chunk_data["embedding"]
        )

        chunks.append(chunk)
    
    db.add_all()
    db.commit()

    for chunk in chunks:
        db.refresh(chunk)

    return chunks

def get_chunks_by_document_id(
    db: Session,
    document_id: int
) -> list[DocumentChunkModel]:
    return (
        db.query(DocumentChunkModel)
         .filter(DocumentChunkModel.document_id == document_id)
         .order_by(DocumentChunkModel.chunk_index.asc())
         .all()
    )