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

#문서 저장 API
@router.post("", response_model=DocumentCreateResponse)
def create_document_api(
    request: DocumentCreateRequest,
    db: Session = Depends(get_db),   
):
    return document_service.create_document(request,db)


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