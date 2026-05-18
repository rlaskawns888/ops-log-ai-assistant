from typing import Optional

from sqlalchemy.orm import Session

from app.models.document import Document

from app.schemas.document_schema import DocumentCreateRequest

class DocumentRepository:
    #문서 DB 저장 
    def save_document(
        self,
        db: Session,
        request: DocumentCreateRequest,    
    ) -> Document:
        document = Document( #요청 schema에서 받은 값을 SQLAlchemy Model로 변경
            title=request.title,
            document_type=request.document_type,
            source=request.source,
            content=request.content
        )

        db.add(document)
        db.flush()

        return document

    #단건 조회 
    def get_document_by_id(
        self,
        db: Session,
        document_id: int,    
    ) -> Optional[Document]:
        return (
            db.query(Document)
            .filter(Document.id == document_id)
            .first()
        )

    #다건 조회
    def get_documents(    
        self,
        db:Session,
        limit: int=20,
        offset: int=0,    
    ) -> list[Document]:
        return (
            db.query(Document)
            .order_by(Document.id.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

