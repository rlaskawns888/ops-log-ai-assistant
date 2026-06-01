from typing import Any, Dict

from app.core.config import settings
from app.clients.openai_client import (
    OpenAIClient,
    OpenAIClientError,
)

class LLMServiceError(Exception):
    pass

class LLMService:
    def __init__(self):
        if settings.llm_provider == "openai":
            self.client = OpenAIClient()
        elif settings.llm_provider == "mock":
            self.client = None
        else:
            raise LLMServiceError(
                f"Unsupported LLM_PROVIDER: {settings.llm_provider}"
            )
        
    async def analyze_log(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> Dict[str, Any]:
        if settings.llm_provider == "mock":
            return self._mock_response()
        
        response_schema = self._build_log_analysis_response_schema()

        try:
            return await self.client.analyze_log(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                response_schema=response_schema
            )
        
        except OpenAIClientError as e:
            raise LLMServiceError(str(e))

        except Exception as e:
            raise LLMServiceError(f"LLM analysis failed: {str(e)}")

    def _mock_response(self) -> Dict[str, Any]:
        return {
            "content": {
                "summary": "Mock 분석 결과입니다. 로그에서 DB connection timeout 가능성이 확인되었습니다.",
                "severity": "HIGH",
                "possibleRootCauses": [
                    {
                        "cause": "DB connection pool 고갈 가능성",
                        "evidence": "로그와 유사 운영 문서에서 connection timeout 및 connection pool 확인 내용이 확인되었습니다."
                    }
                ],
                "safeActions": [
                    {
                        "action": "DB connection pool 사용량을 확인합니다."
                    },
                    {
                        "action": "payment-service 인스턴스 수와 DB 최대 연결 수를 점검합니다."
                    },
                    {
                        "action": "DB slow query, DB CPU 사용률, 네트워크 지연 여부를 확인합니다."
                    }
                ]
            },
            "model_name": "mock-llm",
            "input_token_count": None,
            "output_token_count": None,
            "total_tokens": None,
        }

    def _build_log_analysis_response_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "summary": {
                    "type": "string",
                    "description": "로그 분석 요약"
                },
                "severity": {
                    "type": "string",
                    "enum": ["LOW", "MEDIUM", "HIGH", "CRITICAL", "UNKNOWN"],
                    "description": "장애 심각도"
                },
                "possibleRootCauses": {
                    "type": "array",
                    "description": "가능한 원인 목록",
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "cause": {
                                "type": "string",
                                "description": "가능한 원인"
                            },
                            "evidence": {
                                "type": "string",
                                "description": "해당 원인을 판단한 근거"
                            }
                        },
                        "required": ["cause", "evidence"]
                    }
                },
                "safeActions": {
                    "type": "array",
                    "description": "운영자가 안전하게 수행할 수 있는 조치 목록",
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "action": {
                                "type": "string",
                                "description": "권장 조치"
                            }
                        },
                        "required": ["action"]
                    }
                }
            },
            "required": [
                "summary",
                "severity",
                "possibleRootCauses",
                "safeActions"
            ]
        }