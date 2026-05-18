from sqlalchemy.orm import Session

from app.schemas.document_schema import (
    DocumentCreateRequest, 
    DocumentCreateResponse
)

from app.repositories.document_repository import DocumentRepository
from app.repositories.chunk_repository import DocumentChunkRepository

from app.utils.chunker import split_text_into_chunks
from app.utils.embedding import create_embedding


class DocumentService:
    def __init__(self):
        self.repository = DocumentRepository()
        self.chunk_repository = DocumentChunkRepository()

    # 문서 등록
    def create_document(
        self,
        request: DocumentCreateRequest,
        db: Session,
    ) -> DocumentCreateResponse:
        
        try: 
            #문서 저장
            document = self.repository.save_document(db, request)

            #chunk 분리 (임시)
            chunks = split_text_into_chunks(
                text=request.content,
                chunk_size=500,
                chunk_overlap=80
            )

            chunk_data_list = []

            for index, chunk_content in enumerate(chunks):
                #embedding
                embedding = create_embedding(chunk_content) 

                chunk_data_list.append({
                    "document_id":document.id,
                    "chunk_index":index,
                    "content":chunk_content,
                    "embedding":embedding,
                    "token_count": len(chunk_content.split()),
                    "chunk_metadata": {
                        "title":request.title,
                        "source":request.source,
                        "document_type": request.document_type
                    }
                })

            #문서 저장
            self.chunk_repository.save_document_chunks(
                db,
                chunk_data_list
            )

            db.commit()

            return DocumentCreateResponse(
                documentId=document.id,
                title=document.title,
                documentType=document.document_type,
                source=document.source,
                chunkCount=len(chunks),
                message="문서가 성공적으로 등록되었습니다."
            )
        
        except Exception as e:
            db.rollback()
            raise e
        
        