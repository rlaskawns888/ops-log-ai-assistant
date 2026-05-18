-- =========================================================
-- ops-log-ai-assistant ERD SQL for VSCode vuerd / ERD Editor
-- Database: PostgreSQL
-- Note:
-- 1) 실제 DB 실행 시 embedding은 vector(1536)을 사용하세요.
-- 2) vuerd에서 vector 타입 파싱 오류가 나면 embedding TEXT로 바꿔서 import하세요.
-- =========================================================

CREATE TABLE documents (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    document_type VARCHAR(50) NOT NULL,
    source VARCHAR(500),
    content TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE document_chunks (
    id BIGSERIAL PRIMARY KEY,
    document_id BIGINT NOT NULL,
    chunk_index INTEGER NOT NULL,
    content TEXT NOT NULL,
    embedding vector(1536),
    token_count INTEGER,
    metadata JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_document_chunks_document
        FOREIGN KEY (document_id)
        REFERENCES documents(id)
        ON DELETE CASCADE
);

CREATE TABLE log_analysis_requests (
    id BIGSERIAL PRIMARY KEY,
    request_title VARCHAR(255),
    raw_log TEXT NOT NULL,
    service_name VARCHAR(100),
    environment VARCHAR(50),
    log_level VARCHAR(20),
    status VARCHAR(30) NOT NULL DEFAULT 'PENDING',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE log_analysis_results (
    id BIGSERIAL PRIMARY KEY,
    request_id BIGINT NOT NULL,
    summary TEXT NOT NULL,
    root_cause TEXT,
    recommended_action TEXT,
    severity VARCHAR(20),
    model_name VARCHAR(100),
    prompt_version VARCHAR(50),
    input_token_count INTEGER,
    output_token_count INTEGER,
    total_tokens INTEGER,
    latency_ms INTEGER,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_log_analysis_results_request
        FOREIGN KEY (request_id)
        REFERENCES log_analysis_requests(id)
        ON DELETE CASCADE,

    CONSTRAINT uq_log_analysis_results_request
        UNIQUE (request_id)
);

CREATE TABLE log_analysis_references (
    id BIGSERIAL PRIMARY KEY,
    result_id BIGINT NOT NULL,
    document_chunk_id BIGINT NOT NULL,
    similarity_score DOUBLE PRECISION,
    distance DOUBLE PRECISION,
    rank_order INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_log_analysis_references_result
        FOREIGN KEY (result_id)
        REFERENCES log_analysis_results(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_log_analysis_references_chunk
        FOREIGN KEY (document_chunk_id)
        REFERENCES document_chunks(id)
        ON DELETE CASCADE
);

CREATE TABLE ai_feedbacks (
    id BIGSERIAL PRIMARY KEY,
    result_id BIGINT NOT NULL,
    rating INTEGER,
    feedback_type VARCHAR(50),
    comment TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_ai_feedbacks_result
        FOREIGN KEY (result_id)
        REFERENCES log_analysis_results(id)
        ON DELETE CASCADE,

    CONSTRAINT chk_ai_feedbacks_rating
        CHECK (rating IS NULL OR rating BETWEEN 1 AND 5)
);

-- =========================================================
-- vuerd 파싱 오류 발생 시 대체용
-- 아래처럼 document_chunks.embedding만 TEXT로 바꿔서 import하면 됩니다.
-- 실제 DB에서는 vector(1536)을 유지하세요.
-- =========================================================
-- embedding TEXT
