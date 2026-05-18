from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.document_schema import (
    DocumentCreateRequest,
    DocumentCreateResponse,    
)
from app.schemas.document_search_schema import(
    DocumentSearchRequest,
    DocumentSearchResponse,
)

from app.services.document_service import DocumentService
from app.services.document_search_service import DocumentSearchService


router = APIRouter(
    prefix="/api/documents",
    tags=["Documents"]
)

document_service = DocumentService()
document_search_service = DocumentSearchService()

# {
#   "title": "결제 서비스 DB Timeout 대응 문서",
#   "document_type": "RUNBOOK",
#   "source": "notion",
#   "content": "결제 서비스에서 Database connection timeout이 발생하면 먼저 DB connection pool 사용량을 확인한다. connection pool이 모두 사용 중이면 payment-service 인스턴스 수와 DB 최대 연결 수를 점검한다. 또한 DB slow query, DB CPU 사용률, 네트워크 지연 여부를 함께 확인한다. 장애가 지속되면 payment-service를 재시작하기 전에 현재 요청량과 DB 연결 상태를 먼저 확인해야 한다."
# }
#문서 저장 API
@router.post("", response_model=DocumentCreateResponse)
def create_document_api(
    request: DocumentCreateRequest,
    db: Session = Depends(get_db),   
):
    return document_service.create_document(request,db)


# {
#   "query": "Database connection timeout occurred while processing payment request.",
#   "top_k": 3,
#   "threshold": 0.35
# }
#문서 조회 API
@router.post("/search", response_model=DocumentSearchResponse)
def search_documents(
    request: DocumentSearchRequest,
    db: Session = Depends(get_db)
):
    return document_search_service.search_documents(request, db)


#문서 단건 조회 API
# @router.get("/{document_id}", response_model=DocumentResponse)
# def get_document_api(
#     document_id: int,
#     db: Session = Depends(get_db),    
# ):
#     document = get_document_by_id(db, document_id)

#     return document


#문서 다건 조회 API
# @router.get("", response_model=list[DocumentResponse])
# def get_documents_api(
#     limit: int=20,
#     offset: int=0,
#     db: Session = Depends(get_db)
# ):
#     return get_documents(db, limit=limit, offset=offset)