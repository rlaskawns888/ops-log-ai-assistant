CREATE EXTENSION IF NOT EXISTS vector;

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

CREATE INDEX idx_document_chunks_document_id
ON document_chunks(document_id);

CREATE INDEX idx_log_analysis_requests_status
ON log_analysis_requests(status);

CREATE INDEX idx_log_analysis_results_request_id
ON log_analysis_results(request_id);

CREATE INDEX idx_log_analysis_references_result_id
ON log_analysis_references(result_id);

CREATE INDEX idx_ai_feedbacks_result_id
ON ai_feedbacks(result_id);


-- =========================================================
-- TABLE COMMENTS
-- =========================================================

COMMENT ON TABLE documents IS '운영 문서 원본 정보를 저장하는 테이블';
COMMENT ON TABLE document_chunks IS '운영 문서를 chunk 단위로 분리하고 embedding vector를 저장하는 테이블';
COMMENT ON TABLE log_analysis_requests IS '사용자의 운영 로그 분석 요청 원본을 저장하는 테이블';
COMMENT ON TABLE log_analysis_results IS 'LLM이 생성한 로그 분석 결과를 저장하는 테이블';
COMMENT ON TABLE log_analysis_references IS 'AI 분석 결과가 참고한 문서 chunk 근거 정보를 저장하는 테이블';
COMMENT ON TABLE ai_feedbacks IS 'AI 분석 결과에 대한 사용자 피드백을 저장하는 테이블';


-- =========================================================
-- documents COLUMN COMMENTS
-- =========================================================

COMMENT ON COLUMN documents.id IS '문서 고유 ID';
COMMENT ON COLUMN documents.title IS '운영 문서 제목';
COMMENT ON COLUMN documents.document_type IS '문서 유형. 예: TROUBLESHOOTING, RUNBOOK, INCIDENT_GUIDE';
COMMENT ON COLUMN documents.source IS '문서 출처. 예: internal wiki, markdown file, manual';
COMMENT ON COLUMN documents.content IS '운영 문서 원본 전체 내용';
COMMENT ON COLUMN documents.created_at IS '문서 생성일시';
COMMENT ON COLUMN documents.updated_at IS '문서 수정일시';


-- =========================================================
-- document_chunks COLUMN COMMENTS
-- =========================================================

COMMENT ON COLUMN document_chunks.id IS '문서 chunk 고유 ID';
COMMENT ON COLUMN document_chunks.document_id IS '원본 문서 ID';
COMMENT ON COLUMN document_chunks.chunk_index IS '문서 내 chunk 순서';
COMMENT ON COLUMN document_chunks.content IS 'chunk 본문 내용';
COMMENT ON COLUMN document_chunks.embedding IS 'chunk 내용을 embedding 모델로 변환한 vector 값';
COMMENT ON COLUMN document_chunks.token_count IS 'chunk의 토큰 수';
COMMENT ON COLUMN document_chunks.metadata IS 'chunk 관련 추가 메타데이터. 예: section, page, tags';
COMMENT ON COLUMN document_chunks.created_at IS 'chunk 생성일시';


-- =========================================================
-- log_analysis_requests COLUMN COMMENTS
-- =========================================================

COMMENT ON COLUMN log_analysis_requests.id IS '로그 분석 요청 고유 ID';
COMMENT ON COLUMN log_analysis_requests.request_title IS '로그 분석 요청 제목';
COMMENT ON COLUMN log_analysis_requests.raw_log IS '사용자가 입력한 원본 로그 내용';
COMMENT ON COLUMN log_analysis_requests.service_name IS '로그가 발생한 서비스명';
COMMENT ON COLUMN log_analysis_requests.environment IS '로그 발생 환경. 예: dev, staging, prod';
COMMENT ON COLUMN log_analysis_requests.log_level IS '로그 레벨. 예: INFO, WARN, ERROR';
COMMENT ON COLUMN log_analysis_requests.status IS '분석 요청 처리 상태. 예: PENDING, PROCESSING, COMPLETED, FAILED';
COMMENT ON COLUMN log_analysis_requests.created_at IS '분석 요청 생성일시';
COMMENT ON COLUMN log_analysis_requests.updated_at IS '분석 요청 수정일시';


-- =========================================================
-- log_analysis_results COLUMN COMMENTS
-- =========================================================

COMMENT ON COLUMN log_analysis_results.id IS 'AI 분석 결과 고유 ID';
COMMENT ON COLUMN log_analysis_results.request_id IS '분석 요청 ID';
COMMENT ON COLUMN log_analysis_results.summary IS 'AI가 생성한 로그 분석 요약';
COMMENT ON COLUMN log_analysis_results.root_cause IS 'AI가 추정한 장애 또는 오류 원인';
COMMENT ON COLUMN log_analysis_results.recommended_action IS 'AI가 제안한 조치 방법';
COMMENT ON COLUMN log_analysis_results.severity IS 'AI가 판단한 심각도. 예: LOW, MEDIUM, HIGH, CRITICAL';
COMMENT ON COLUMN log_analysis_results.model_name IS '분석에 사용한 LLM 모델명';
COMMENT ON COLUMN log_analysis_results.prompt_version IS '분석에 사용한 프롬프트 버전';
COMMENT ON COLUMN log_analysis_results.input_token_count IS 'LLM 요청 입력 토큰 수';
COMMENT ON COLUMN log_analysis_results.output_token_count IS 'LLM 응답 출력 토큰 수';
COMMENT ON COLUMN log_analysis_results.created_at IS 'AI 분석 결과 생성일시';


-- =========================================================
-- log_analysis_references COLUMN COMMENTS
-- =========================================================

COMMENT ON COLUMN log_analysis_references.id IS 'AI 분석 근거 고유 ID';
COMMENT ON COLUMN log_analysis_references.result_id IS 'AI 분석 결과 ID';
COMMENT ON COLUMN log_analysis_references.document_chunk_id IS 'AI 답변 생성 시 참고한 문서 chunk ID';
COMMENT ON COLUMN log_analysis_references.similarity_score IS '사용자 로그와 문서 chunk 간 유사도 점수';
COMMENT ON COLUMN log_analysis_references.distance IS 'vector 검색에서 계산된 거리 값. 낮을수록 유사함';
COMMENT ON COLUMN log_analysis_references.rank_order IS '검색 결과 순위';
COMMENT ON COLUMN log_analysis_references.created_at IS '근거 정보 생성일시';


-- =========================================================
-- ai_feedbacks COLUMN COMMENTS
-- =========================================================

COMMENT ON COLUMN ai_feedbacks.id IS '사용자 피드백 고유 ID';
COMMENT ON COLUMN ai_feedbacks.result_id IS '피드백 대상 AI 분석 결과 ID';
COMMENT ON COLUMN ai_feedbacks.rating IS '사용자 평점. 1점부터 5점까지 저장';
COMMENT ON COLUMN ai_feedbacks.feedback_type IS '피드백 유형. 예: GOOD, BAD, WRONG_REFERENCE, HALLUCINATION';
COMMENT ON COLUMN ai_feedbacks.comment IS '사용자가 남긴 상세 피드백';
COMMENT ON COLUMN ai_feedbacks.created_at IS '피드백 생성일시';