from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.document_schema import (
    DocumentCreateRequest,
    DocumentCreateResponse,
    DocumentResponse
)
from app.services.document_service import create_document
from app.repositories.document_repository import (
    get_document_by_id,
    get_documents
)

router = APIRouter(
    prefix="/api/documents",
    tags=["Documents"]
)

#문서 저장 API
@router.post("", response_model=DocumentCreateResponse)
def create_document_api(
    request: DocumentCreateRequest,
    db: Session = Depends(get_db),   
):
    return create_document(request, db)

#문서 단건 조회 API
@router.get("/{document_id}", response_model=DocumentResponse)
def get_document_api(
    document_id: int,
    db: Session = Depends(get_db),    
):
    docuemnt = get_document_by_id(db, document_id)

#문서 다건 조회 API
@router.get("", response_model=list[DocumentResponse])
def get_documents_api(
    limit: int=20,
    offset: int=0,
    db: Session = Depends(get_db)
):
    return get_documents(db, limit=limit, offset=offset)