import json


def call_llm(
    system_prompt: str,
    user_prompt: str
) -> str:
    """
    TODO:
    실제 구현에서는 OpenAI, Claude, Gemini 같은 LLM API를 호출한다.

    현재는 9단계 흐름 테스트를 위한 더미 JSON 문자열을 반환한다.
    """

    dummy_response = {
        "analysisStatus": "SUCCESS",
        "summary": "payment-service에서 결제 요청 처리 중 Database connection timeout이 발생했습니다.",
        "severity": "HIGH",
        "confidence": "MEDIUM",
        "confirmedFacts": [
            {
                "fact": "로그에서 Database connection timeout이 발생했습니다.",
                "evidence": [
                    {
                        "documentId": 1,
                        "chunkId": 1,
                        "source": "notion",
                        "reason": "제공된 운영 문서에 DB timeout 발생 시 확인 절차가 포함되어 있습니다."
                    }
                ]
            }
        ],
        "possibleRootCauses": [
            {
                "cause": "DB 상태 이상, connection pool 사용량 증가, slow query 발생 가능성이 있습니다.",
                "confidence": "MEDIUM",
                "evidence": [
                    {
                        "documentId": 1,
                        "chunkId": 1,
                        "source": "notion",
                        "reason": "문서에서 DB 상태, connection pool 사용량, slow query 여부를 확인하라고 안내하고 있습니다."
                    }
                ]
            }
        ],
        "safeActions": [
            {
                "action": "DB 상태를 확인합니다.",
                "reason": "서비스 변경 없이 현재 상태를 확인하는 안전한 조치입니다.",
                "evidence": [
                    {
                        "documentId": 1,
                        "chunkId": 1,
                        "source": "notion",
                        "reason": "문서에서 DB 상태 확인을 안내하고 있습니다."
                    }
                ]
            },
            {
                "action": "connection pool 사용량을 확인합니다.",
                "reason": "설정 변경 없이 사용량만 확인하는 안전한 조치입니다.",
                "evidence": [
                    {
                        "documentId": 1,
                        "chunkId": 1,
                        "source": "notion",
                        "reason": "문서에서 connection pool 사용량 확인을 안내하고 있습니다."
                    }
                ]
            },
            {
                "action": "slow query 발생 여부를 확인합니다.",
                "reason": "조회성 점검이므로 운영 변경을 발생시키지 않습니다.",
                "evidence": [
                    {
                        "documentId": 1,
                        "chunkId": 1,
                        "source": "notion",
                        "reason": "문서에서 slow query 여부 확인을 안내하고 있습니다."
                    }
                ]
            }
        ],
        "approvalRequiredActions": [],
        "missingInformation": [
            "DB 서버 상태 지표",
            "connection pool 실제 사용률",
            "slow query 로그",
            "최근 배포 이력"
        ]
    }

    return json.dumps(dummy_response, ensure_ascii=False)