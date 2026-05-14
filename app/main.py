from fastapi import FastAPI

app = FastAPI(
    title="Ops Log Ai Assistant",
    description="운영 로그 분석하고 관련 운영 문서를 기반으로 원인과 해결책을 제안하는 AI 서비스",
    version="1.0.0"
)

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "Ops Log AI Assistant is running"
    }