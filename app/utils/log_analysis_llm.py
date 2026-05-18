import json

from app.prompts.log_analysis_prompt import (
    SYSTEM_PROMPT,
    build_log_analysis_user_prompt
)
from app.utils.llm_client import call_llm


def generate_log_analysis(
    raw_log: str,
    service_name: str,
    environment: str,
    log_level: str,
    preprocessed_log: dict,
    similar_chunks: list[dict]
) -> dict:
    """
        운영 로그 분석 LLM 호출 함수.

        역할:
        1. System Prompt 적용
        2. User Prompt 생성
        3. LLM 호출
        4. JSON 응답 파싱
        5. 파싱 실패 시 안전한 fallback 반환
    """

    user_prompt = build_log_analysis_user_prompt(
        raw_log=raw_log,
        service_name=service_name,
        environment=environment,
        log_level=log_level,
        preprocessed_log=preprocessed_log,
        similar_chunks=similar_chunks
    )

    response_text = call_llm(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=user_prompt
    )

    try:
        return json.loads(response_text)

    except json.JSONDecodeError:
        return {
            "analysisStatus": "FAILED",
            "summary": "LLM 응답이 올바른 JSON 형식이 아닙니다.",
            "severity": "UNKNOWN",
            "confidence": "LOW",
            "confirmedFacts": [],
            "possibleRootCauses": [],
            "safeActions": [],
            "approvalRequiredActions": [],
            "missingInformation": [
                "LLM returned invalid JSON format."
            ]
        }