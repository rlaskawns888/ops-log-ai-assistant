from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    #Database
    database_url: str

    #Provider
    llm_provider: str = "mock"
    embedding_provider: str = "openai"

    #OpenAI
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-5.4-mini"
    openai_embedding_mode: str = "text-embedding-3-small"
    openai_timeout_seconds: float = 20.0
    openai_max_retries: int = 1

    #Vector Search
    runbook_search_top_k: int = 3

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()