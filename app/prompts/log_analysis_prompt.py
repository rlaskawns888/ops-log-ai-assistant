import json

from app.schemas.log_analysis_schema import LogAnalysisRequest


def create_system_prompt() -> str:
    return """
        당신은 운영 로그를 분석하는 AI 어시스턴트입니다.
        사용자가 입력한 로그와 참고 운영 문서를 기반으로 장애 가능성을 분석합니다.

        반드시 JSON 형식으로만 응답하세요.
    """

def create_user_prompt(
    request: LogAnalysisRequest,
    similar_chunks: list[dict]
) -> str:
    return f"""
        [분석 요청 제목]
        {request.request_title}

        [서비스명]
        {request.service_name}

        [환경]
        {request.environment}

        [로그 레벨]
        {request.log_level}

        [원본 로그]
        {request.raw_log}

        [참고 운영 문서 chunk]
        {json.dumps(similar_chunks, ensure_ascii=False, indent=2)}
    """