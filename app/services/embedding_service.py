from typing import List

from app.core.config import settings
from app.clients.openai_embedding_client import (
    OpenAIEmbeddingClient,
    EmbeddingClientError,
)
from app.clients.mock_embedding_client import MockEmbeddingClient

class EmbeddingServiceError(Exception):
    pass

class EmbeddingService:
    def __init__(self):
        if settings.embedding_provider == "openai":
            self.client = OpenAIEmbeddingClient()
        elif settings.embedding_provider == "mock":
            self.client = MockEmbeddingClient()
        else:
            raise EmbeddingServiceError(
                f"Unsupported EMBEDDING_PROVIDER: {settings.embedding_provider}"
            )
        
    async def embed_text(self, text: str) -> List[float]:
        if text is None or text.strip() == "":
            raise EmbeddingServiceError("Embedding text is empty.")

        try:
            return await self.client.create_embedding(text)
        except EmbeddingClientError as e:
            raise EmbeddingServiceError(str(e))
        except Exception as e:
            raise EmbeddingServiceError(
                f"Failed to create embedding: {str(e)}"
            )
