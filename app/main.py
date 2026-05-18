import logging

from fastapi import FastAPI
from sqlalchemy import text

from app.core.database import SessionLocal
from app.routers import document_router
from app.routers import log_analysis_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)

app = FastAPI(
    title="Ops Log Ai Assistant",
    description="운영 로그 분석하고 관련 운영 문서를 기반으로 원인과 해결책을 제안하는 AI 서비스",
    version="1.0.0"
)

# 서버 연결 확인
@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "Ops Log AI Assistant is running"
    }

#DB 연결 확인
@app.get("/health/db")
def database_health_check():
    db = SessionLocal()

    try:
        db.execute(text("SELECT 1"))
        
        return {
            "status": "ok",
            "message": "Database connection is successful"
        }
    finally:
        db.close()
    

app.include_router(document_router.router)
app.include_router(log_analysis_router.router)