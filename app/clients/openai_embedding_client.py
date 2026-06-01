from typing import List

from openai import AsyncOpenAI, APITimeoutError, APIConnectionError, APIStatusError

from app.core.config import settings

class EmbeddingClientError(Exception):
    pass

class OpenAIEmbeddingClient:
    def __init__(self):
        if not settings.openai_api_key:
            raise EmbeddingClientError("OPENAI_API_KEY is not configured.")
        
        self.client = AsyncOpenAI(
            api_key=settings.openai_api_key,
            timeout=settings.openai_timeout_seconds,
            max_retries=settings.openai_max_retries,   
        )

        self.model = settings.openai_embedding_mode

    async def create_embedding(self, text: str) -> List[float]:
        if text is None or text.strip() == "":
            raise EmbeddingClientError("Embedding input text is empty.")
        
        try:
            response = await self.client.embeddings.create(
                model=self.model,
                input=text,
            )

            return response.data[0].embedding

        except APITimeoutError as e:
            raise EmbeddingClientError(
                f"OpenAI embedding request timed out: {str(e)}"
            )

        except APIConnectionError as e:
            raise EmbeddingClientError(
                f"OpenAI embedding connection error: {str(e)}"
            )

        except APIStatusError as e:
            raise EmbeddingClientError(
                f"OpenAI embedding API status error: status_code={e.status_code}"
            )

        except Exception as e:
            raise EmbeddingClientError(
                f"Unexpected embedding error: {str(e)}"
            )
