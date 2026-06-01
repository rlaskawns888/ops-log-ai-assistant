from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.schemas.document_search_schema import (
    DocumentSearchRequest,
    DocumentSearchResponse,
    DocumentSearchResult
)

from app.repositories.document_search_repository import DocumentSearchRepository

from app.services.embedding_service import (
    EmbeddingService,
    EmbeddingServiceError
)

class DocumentSearchService:
    def __init__(self):
        self.repository = DocumentSearchRepository()
        self.embedding_service = EmbeddingService()

    #문서 조회
    async def search_documents(
        self,
        request: DocumentSearchRequest,
        db: Session
    ) -> DocumentSearchResponse:
        try:
            #embedding
            query_embedding = await self.embedding_service.embed_text(request.query) 

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
        
        except EmbeddingServiceError as e:
            raise HTTPException(
                status_code=502,
                detail=f"Failed to create document embedding: {str(e)}"
            )
