from sqlalchemy.orm import Session

from app.schemas.document_schema import DocumentCreateRequest, DocumentCreateResponse
from app.repositories.document_repository import save_document
from app.repositories.chunk_repository import save_document_chunks
from app.services.embedding_service import create_embedding
from app.utils.text_splitter import split_text

# 문서 등록 API
def create_document(
    request: DocumentCreateRequest,
    db: Session,
) -> DocumentCreateResponse:
    document = save_document(db, request) #DB - 문서 저장 

    chunks = split_text(request.content) #chunk 분리

    chunk_data_list = []

    for index, chunk in enumerate(chunks):
        embedding = create_embedding(chunk) #embedding

        chunk_data_list.append({
            "document_id": document.id,
            "chunk_index": index,
            "content": chunk,
            "embedding": embedding
        })
    
    save_document_chunks(db, chunk_data_list) #DB - 문서 > Chunk 저장

    return DocumentCreateResponse(
        document_id=document.id,
        title=document.title,
        document_type=document.document_type,
        chunk_count=len(chunks)
    )