CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS log_events (
    id BIGSERIAL PRIMARY KEY,
    service_name VARCHAR(100) NOT NULL,
    environment VARCHAR(50) NOT NULL,
    level VARCHAR(20) NOT NULL,
    message TEXT NOT NULL,
    stack_trace TEXT,
    trace_id VARCHAR(100),
    request_id VARCHAR(100),
    status_code INTEGER,
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    embedding vector(3)
);