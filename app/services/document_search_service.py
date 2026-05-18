from sqlalchemy.orm import Session

from app.schemas.document_search_schema import (
    DocumentSearchRequest,
    DocumentSearchResponse,
    DocumentSearchResult
)

from app.repositories.document_search_repository import DocumentSearchRepository

from app.utils.embedding import create_embedding

class DocumentSearchService:
    def __init__(self):
        self.repository = DocumentSearchRepository()

    #문서 조회
    def search_documents(
        self,
        request: DocumentSearchRequest,
        db: Session
    ) -> DocumentSearchResponse:
        #embedding
        query_embedding = create_embedding(request.query) 

        #유사한 문서 조회
        rows = self.repository.search_similar_chunks(
            db=db,
            query_embedding=query_embedding,
            top_k=request.top_k,
            threshold=request.threshold
        )
        
        results = [
            DocumentSearchResult(
                documentId=row.document_id,
                chunkId=row.chunk_id,
                title=row.title,
                source=row.source,
                content=row.content,
                distance=float(row.distance)
            )
            for row in rows
        ]

        return DocumentSearchResponse(
            query=request.query,
            top_k=request.top_k,
            threshold=request.threshold,
            results=results
        )