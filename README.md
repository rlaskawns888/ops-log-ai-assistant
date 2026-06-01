# LogOps AI Assistant

## 1. 프로젝트를 만든 이유

운영 업무에서는 장애가 발생했을 때 로그를 확인하고, 관련 문서를 찾고, 조치 방법을 정리하는 과정이 반복된다.

이 프로젝트는 운영 로그 입력값을 전처리하고, 관련 운영 문서를 검색한 뒤, LLM 응답 결과를 저장하는 API 서버를 구현하기 위해 만들었다.

기본 흐름은 다음과 같다.

```text
운영 로그 입력
→ 로그 전처리
→ 관련 운영 문서 검색
→ LLM 분석 요청
→ 분석 결과 저장
→ 피드백 저장
```

---

## 2. 주요 기능

- 운영 문서 등록
- 운영 문서 chunk 분리
- embedding 생성 및 저장
- PostgreSQL + pgvector 기반 유사 문서 검색
- 운영 로그 전처리
- OpenAI API 기반 로그 분석
- JSON 형식 분석 결과 반환
- 분석 요청 및 결과 저장
- 분석 결과에 사용된 참조 문서 저장
- 사용자 피드백 저장

---

## 3. 전체 아키텍처

```text
Client
  |
  | HTTP Request
  v
FastAPI
  |
  | 1. 운영 문서 등록
  v
Document Service
  |
  | chunk 분리 / embedding 생성
  v
PostgreSQL + pgvector
  |
  | 2. 로그 분석 요청
  v
Log Analysis Service
  |
  | 로그 전처리
  v
Runbook Search Service
  |
  | 관련 운영 문서 검색
  v
LLM Service
  |
  | OpenAI API 호출
  v
PostgreSQL
  |
  | 분석 요청 / 분석 결과 / 참조 문서 / 피드백 저장
```

로그 분석 요청 처리 순서:

```text
1. 사용자가 운영 로그를 입력한다.
2. 서버에서 로그를 전처리한다.
3. 로그 내용과 관련 있는 운영 문서를 검색한다.
4. 검색된 문서를 context로 구성한다.
5. 로그 원문, 전처리 결과, context를 LLM에 전달한다.
6. LLM 응답을 JSON 형식으로 받는다.
7. 분석 요청, 분석 결과, 참조 문서를 DB에 저장한다.
```

---

## 4. 기술 스택

### Backend

- Python
- FastAPI
- Pydantic
- SQLAlchemy

### Database

- PostgreSQL
- pgvector

### AI

- OpenAI API
- Embedding
- RAG
- JSON structured output

### Infra

- Docker
- Docker Compose

---

## 5. RAG 처리 흐름

이 프로젝트에서는 운영 문서를 검색한 뒤, 검색 결과를 LLM 입력 context로 사용한다.

### 문서 등록 흐름

```text
1. 운영 문서를 등록한다.
2. 문서를 chunk 단위로 분리한다.
3. 각 chunk의 embedding을 생성한다.
4. chunk 원문, metadata, embedding을 PostgreSQL에 저장한다.
```

저장되는 chunk 정보:

```text
- document_id
- chunk_index
- content
- embedding
- source
- created_at
```

### 로그 분석 시 검색 흐름

```text
1. 로그 분석 요청이 들어온다.
2. 로그 원문 또는 전처리된 키워드를 embedding으로 변환한다.
3. pgvector를 사용해 유사한 운영 문서 chunk를 검색한다.
4. 검색된 chunk를 LLM context로 구성한다.
5. LLM 응답 생성 시 검색된 문서를 함께 전달한다.
```

---

## 6. OpenAI 연동 구조

OpenAI API는 로그 분석 결과를 생성하는 단계에서 사용한다.

LLM에 전달하는 데이터는 다음과 같다.

```text
1. 로그 원문
2. 로그 전처리 결과
3. pgvector로 검색된 운영 문서 context
```

### 로그 전처리 결과 예시

```json
{
  "errorCount": 2,
  "warnCount": 1,
  "exceptions": [
    "SQLTransientConnectionException"
  ],
  "httpStatusCodes": [
    504
  ],
  "keywords": [
    "timeout",
    "HikariPool",
    "connection"
  ]
}
```

### LLM 응답 형식 예시

```json
{
  "summary": "payment-service에서 DB connection pool 관련 오류가 발생했습니다.",
  "severity": "HIGH",
  "incidentType": "DB_CONNECTION_ERROR",
  "rootCauseCandidates": [
    "DB connection pool exhaustion",
    "Slow query",
    "Transaction lock"
  ],
  "affectedServices": [
    "payment-service"
  ],
  "recommendedActions": [
    "HikariCP active connection 수 확인",
    "DB slow query 확인",
    "최근 배포 여부 확인"
  ],
  "preventionActions": [
    "connection pool metric 모니터링 추가",
    "slow query alert 설정"
  ],
  "incidentReport": "장애 보고서 내용",
  "confidence": 0.82
}
```

### LLM Provider

개발 환경에서는 mock 응답을 사용할 수 있고, 실제 분석 시에는 OpenAI API를 호출한다.

```env
LLM_PROVIDER=mock
```

```env
LLM_PROVIDER=openai
```

---

## 7. API 명세

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/runbooks/documents` | 운영 문서 등록 |
| POST | `/api/runbooks/search` | 유사 운영 문서 검색 |
| POST | `/api/logs/analyze` | 운영 로그 분석 |
| GET | `/api/logs/analysis/{id}` | 로그 분석 결과 조회 |
| POST | `/api/feedbacks` | 분석 결과 피드백 저장 |

---

### 7.1 운영 문서 등록

```http
POST /api/runbooks/documents
```

Request

```json
{
  "title": "DB Connection Pool 장애 대응 가이드",
  "source": "runbook/db-connection-pool.md",
  "content": "DB connection pool 고갈이 발생하면 active connection 수와 slow query를 먼저 확인한다."
}
```

Response

```json
{
  "documentId": 1,
  "chunkCount": 3
}
```

---

### 7.2 유사 운영 문서 검색

```http
POST /api/runbooks/search
```

Request

```json
{
  "query": "HikariPool connection timeout",
  "topK": 5
}
```

Response

```json
{
  "results": [
    {
      "documentId": 1,
      "chunkId": 3,
      "title": "DB Connection Pool 장애 대응 가이드",
      "source": "runbook/db-connection-pool.md",
      "content": "DB connection pool 고갈이 발생하면 active connection 수를 확인한다.",
      "distance": 0.18
    }
  ]
}
```

---

### 7.3 운영 로그 분석

```http
POST /api/logs/analyze
```

Request

```json
{
  "serviceName": "payment-service",
  "environment": "production",
  "logText": "ERROR HikariPool-1 - Connection is not available, request timed out after 30000ms.",
  "occurredAt": "2026-06-01T10:30:00"
}
```

Response

```json
{
  "analysisId": 1,
  "summary": "payment-service에서 DB connection pool 관련 오류가 발생했습니다.",
  "severity": "HIGH",
  "incidentType": "DB_CONNECTION_ERROR",
  "rootCauseCandidates": [
    "DB connection pool exhaustion",
    "Slow query",
    "Transaction lock"
  ],
  "recommendedActions": [
    "HikariCP active connection 수 확인",
    "DB slow query 확인",
    "최근 배포 여부 확인"
  ],
  "references": [
    {
      "documentId": 1,
      "chunkId": 3,
      "title": "DB Connection Pool 장애 대응 가이드",
      "source": "runbook/db-connection-pool.md",
      "distance": 0.18
    }
  ]
}
```

---

### 7.4 분석 결과 조회

```http
GET /api/logs/analysis/{id}
```

Response

```json
{
  "analysisId": 1,
  "request": {
    "serviceName": "payment-service",
    "environment": "production",
    "logText": "ERROR HikariPool-1 - Connection is not available..."
  },
  "result": {
    "summary": "payment-service에서 DB connection pool 관련 오류가 발생했습니다.",
    "severity": "HIGH",
    "incidentType": "DB_CONNECTION_ERROR",
    "recommendedActions": [
      "HikariCP active connection 수 확인",
      "DB slow query 확인"
    ]
  },
  "references": [
    {
      "documentId": 1,
      "chunkId": 3,
      "source": "runbook/db-connection-pool.md"
    }
  ]
}
```

---

### 7.5 피드백 저장

```http
POST /api/feedbacks
```

Request

```json
{
  "analysisResultId": 1,
  "feedbackType": "HELPFUL",
  "comment": "원인 후보와 확인 순서가 도움이 됐습니다."
}
```

Response

```json
{
  "feedbackId": 1
}
```

---

## 8. DB 구조

### documents

운영 문서의 기본 정보를 저장한다.

```text
- id
- title
- source
- created_at
```

---

### document_chunks

운영 문서를 chunk 단위로 나눈 결과와 embedding을 저장한다.

```text
- id
- document_id
- chunk_index
- content
- embedding
- created_at
```

---

### log_analysis_requests

로그 분석 요청 정보를 저장한다.

```text
- id
- service_name
- environment
- log_text
- occurred_at
- created_at
```

---

### log_analysis_results

LLM을 통해 생성된 분석 결과를 저장한다.

```text
- id
- request_id
- summary
- severity
- incident_type
- root_cause_candidates
- affected_services
- recommended_actions
- prevention_actions
- incident_report
- confidence
- model_name
- prompt_version
- latency_ms
- total_tokens
- created_at
```

---

### log_analysis_references

분석 결과 생성에 사용된 운영 문서 chunk 정보를 저장한다.

```text
- id
- result_id
- document_chunk_id
- similarity_score
- distance
- rank_order
- created_at
```

---

### ai_feedbacks

분석 결과에 대한 사용자 피드백을 저장한다.

```text
- id
- result_id
- feedback_type
- comment
- created_at
```

---

## 9. 실행 방법

### 9.1 Repository clone

```bash
git clone https://github.com/your-name/logops-ai-assistant.git
cd logops-ai-assistant
```

### 9.2 환경 변수 파일 생성

```bash
cp .env.example .env
```

### 9.3 Docker Compose 실행

```bash
docker-compose up -d
```

### 9.4 Python 패키지 설치

```bash
pip install -r requirements.txt
```

### 9.5 FastAPI 실행

```bash
uvicorn app.main:app --reload
```

### 9.6 Swagger 접속

```text
http://localhost:8000/docs
```

---

## 10. 환경 변수 설정

`.env.example`

```env
APP_NAME=LogOps AI Assistant
APP_ENV=local

DATABASE_URL=postgresql://postgres:postgres@localhost:5432/logops_ai

OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4.1-mini

LLM_PROVIDER=mock

EMBEDDING_MODEL=text-embedding-3-small

RAG_TOP_K=5
RAG_DISTANCE_THRESHOLD=0.35

PROMPT_VERSION=v1
```

실제 OpenAI API를 사용할 경우:

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=your_openai_api_key
```

`.env` 파일은 GitHub에 업로드하지 않는다.