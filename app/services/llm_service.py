#LLM API 호출
def generate_log_analysis(
    log_message: str,
    similar_chunks: list[dict]
) -> dict:
    """
        TODO:
        실제 구현에서는 LLM API를 호출해서 로그 분석 결과를 생성한다.

        현재는 전체 흐름 테스트를 위한 더미 응답을 반환한다.
    """

    return {
        "summary": "로그에서 장애 가능성이 감지되었습니다.",
        "root_cause": "관련 운영 문서를 기반으로 원인을 분석해야 합니다.",
        "recommended_action": "유사 문서를 참고하여 서비스 상태와 인프라 지표를 확인하세요.",
        "severity": "MEDIUM",
        "model_name": "dummy-llm",
        "prompt_version": "v1",
        "input_token_count": None,
        "output_token_count": None
    }