from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings

engine = create_engine( #Python과 PostgreSQL 연결
    settings.database_url, 
    pool_pre_ping=True #DB 살아있는지 확인
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base() 
#SQLAlchemy model들이 상속받을 부모 클래스
# 즉, Base를 상속받은 클래스 = DB 테이블과 연결될 모델

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()