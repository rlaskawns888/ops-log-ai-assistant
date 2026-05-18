import re
from typing import Dict, Any, List

class LogPreprocessor:
    #원본 로그 문자열을 받아서 LLM 분석에 유용한 구조화된 정보를 추출
    def preprocess(self, raw_log: str) -> Dict[str, Any]:
        error_count = self._count_keyword(raw_log, "ERROR")
        warn_count = self._count_keyword(raw_log, "WARN")

        exception_names = self._extract_exception_names(raw_log)
        http_status_codes = self._extract_http_status_codes(raw_log)
        service_names = self._extract_service_names(raw_log)
        timestamps = self._extract_timestamps(raw_log)

        has_timeout = self._contains_timeout(raw_log)

        has_database_keyword = self._contains_database_keyword(raw_log)

        return {
            "errorCount": error_count,
            "warnCount": warn_count,
            "exceptionNames": exception_names,
            "httpStatusCodes": http_status_codes,
            "hasTimeout": has_timeout,
            "hasDatabaseKeyword": has_database_keyword,
            "serviceNames": service_names,
            "timestamps": timestamps,
            "firstTimestamp": timestamps[0] if timestamps else None,
            "lastTimestamp": timestamps[-1] if timestamps else None,
        }


    #특정 키워드가 카운트 ex) ERROR, WARN            
    def _count_keyword(self, text: str, keyword: str) -> int: 

        return len(re.findall(rf"\b{keyword}\b", text, re.IGNORECASE))


    #Exception 이름 추출 ex) NullPointerException, SQLTimeoutException
    def _extract_exception_names(self, text: str) -> List[str]:
        pattern = r"\b[A-Za-z0-9_]*Exception\b"
        matches = re.findall(pattern, text)

        return list(set(matches))
    

    #HTTP status code를 추출한 ex) HTTP 500, status=503, response status 404
    def _extract_http_status_codes(self, text: str) -> List[int]:
        pattern = r"\b(?:HTTP\s*)?(status[=: ]*)?([1-5][0-9]{2})\b"
        matches = re.findall(pattern, text, re.IGNORECASE)

        status_codes = []

        for match in matches:
            code = int(match[1])

            if 100 <= code <= 599:
                status_codes.append(code)

        return list(set(status_codes))


    #timeout 관련 표현이 있는지 확인
    def _contains_timeout(self, text: str) -> bool:
        timeout_keywords = [
            "timeout",
            "timed out",
            "connection timeout",
            "read timeout",
            "query timeout"
        ]

        lower_text = text.lower()

        return any(keyword in lower_text for keyword in timeout_keywords)
    

    #DB 관련 키워드가 있는지 확인
    def _contains_database_keyword(self, text: str) -> bool:        
        database_keywords = [
            "database",
            "db",
            "sql",
            "query",
            "connection",
            "jdbc",
            "postgres",
            "mysql",
            "deadlock",
            "connection pool"
        ]

        lower_text = text.lower()

        return any(keyword in lower_text for keyword in database_keywords)


    #service name 추출 ex) payment-service, order-service
    #여기서는 '-service'로 끝나는 문자열을 서비스명으로 본다.
    def _extract_service_names(self, text: str) -> List[str]:
        pattern = r"\b[a-zA-Z0-9_-]+-service\b"
        matches = re.findall(pattern, text)

        return list(set(matches))


    #timestamp 추출 ex) 026-05-18 10:15:23
    def _extract_timestamps(self, text: str) -> List[str]:
        pattern = r"\b\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}\b"
        matches = re.findall(pattern, text)

        return matches