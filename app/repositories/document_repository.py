from typing import Optional

from sqlalchemy.orm import Session

from app.models.document import DocumentModel
from app.schemas.document_schema import DocumentCreateRequest

#문서 DB 저장 
def save_document(
    db: Session,
    request: DocumentCreateRequest,    
) -> DocumentModel:
    document = DocumentModel( #요청 schema에서 받은 값을 SQLAlchemy Model로 변경
        title=request.title,
        document_type=request.document_type,
        source=request.source,
        content=request.content
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document

#단건 조회 
def get_document_by_id(
    db: Session,
    document_id: int,    
) -> Optional[DocumentModel]:
    return (
        db.query(DocumentModel)
         .filter(DocumentModel.id == document_id)
         .first()
    )

#다건 조회
def get_documents(    
    db:Session,
    limit: int=20,
    offset: int=0,    
) -> list[DocumentModel]:
    return (
        db.query(DocumentModel)
         .order_by(DocumentModel.id.desc())
         .offset(offset)
         .limit(limit)
         .all()
    )

