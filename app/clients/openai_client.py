import json
from typing import Any, Dict

from openai import AsyncOpenAI, APITimeoutError, APIConnectionError, APIStatusError

from app.core.config import settings

class OpenAIClientError(Exception):
    pass

class OpenAIClient:
    def __init__(self):
        if not settings.openai_api_key:
            raise OpenAIClientError("OPENAI_API_KEY is not configured.")
        
        self.client = AsyncOpenAI( #OpenAI Python SDK는 비동기 클라이언트
            api_key=settings.openai_api_key,
            timeout=settings.openai_timeout_seconds,
            max_retries=settings.openai_max_retries,
        )
        self.model = settings.openai_model
    
    async def analyze_log(
        self,
        system_prompt: str,
        user_prompt: str,
        response_schema: Dict[str, Any],
    ) -> Dict[str, Any]:
        try:
            response = await self.client.responses.create(
                model=self.model,
                input=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": user_prompt,
                    },
                ],
                text={ #응답 형태 고정
                    "format": {
                        "type": "json_schema",
                        "name": "log_analysis_result",
                        "schema": response_schema,
                        "strict": True,
                    }
                },
            )

            raw_text = response.output_text

            try:
                parsed = json.loads(raw_text)
            except json.JSONDecodeError as e:
                raise OpenAIClientError(
                    f"Failed to parse OpenAI response as JSON: {str(e)}"
                )

            usage = getattr(response, "usage", None)

            return {
                "content": parsed,
                "model_name": self.model,
                "input_token_count": getattr(usage, "input_tokens", None) if usage else None,
                "output_token_count": getattr(usage, "output_tokens", None) if usage else None,
                "total_tokens": getattr(usage, "total_tokens", None) if usage else None,
            }

        except APITimeoutError as e:
            raise OpenAIClientError(f"OpenAI request timed out: {str(e)}")

        except APIConnectionError as e:
            raise OpenAIClientError(f"OpenAI connection error: {str(e)}")

        except APIStatusError as e:
            raise OpenAIClientError(
                f"OpenAI API status error: status_code={e.status_code}, response={e.response}"
            )

        except OpenAIClientError:
            raise

        except Exception as e:
            raise OpenAIClientError(f"Unexpected OpenAI error: {str(e)}")

