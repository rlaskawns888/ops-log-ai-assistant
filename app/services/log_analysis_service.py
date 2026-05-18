import logging, json

from sqlalchemy.orm import Session

from app.schemas.log_analysis_schema import (
    LogAnalysisRequest, 
    LogAnalysisResponse,
    SimilarChunkResponse,
)
from app.repositories.log_analysis_repository import LogAnalysisRepository
from app.repositories.document_search_repository import DocumentSearchRepository

from app.utils.log_analysis_llm import generate_log_analysis

from app.utils.log_preprocessor import LogPreprocessor
from app.utils.embedding import create_embedding


log = logging.getLogger(__name__)


class LogAnalysisService:
    def __init__(self):
        self.log_analysis_repository = LogAnalysisRepository()
        self.document_search_repository = DocumentSearchRepository()
        self.log_preprocessor = LogPreprocessor()

    def analyze_log(
            self, 
            request: LogAnalysisRequest, 
            db:Session
    ) -> LogAnalysisResponse:
        #로그 전처리
        preprocessed_log = self.log_preprocessor.preprocess(request.raw_log)

        #분석 요청 저장
        saved_request = self.log_analysis_repository.save_analysis_request(
            db=db,
            request=request,
            status="PENDING"
        )

        #전처리된 로그 embedding
        query_embedding = create_embedding(preprocessed_log) 

        #관련 운영 문서 chunk검색
        similar_chunks = self.document_search_repository.search_similar_chunks( 
            db=db,
            query_embedding=query_embedding,
            top_k=request.top_k,
            threshold=request.threshold
        )

        #검색 결과 응답 객체 변환
        referenced_chunks = []

        for index, row in enumerate(similar_chunks, start=1):
            distance = float(row.distance) if row.distance is not None else None

            referenced_chunks.append(
                SimilarChunkResponse(
                    chunk_id=row.chunk_id,
                    document_id=row.document_id,
                    title=getattr(row, "title", None),
                    content=row.content,
                    distance=distance,
                    similarity_score=1 - distance if distance is not None else None,
                    rank_order=index
                )
            )

        #검색 결과가 없으면 LLM 호출하지 않음
        if not similar_chunks:
            self.log_analysis_repository.update_analysis_request_status(
                db=db,
                request_id=saved_request.id,
                status="INSUFFICIENT_CONTEXT"
            )

            self.log_analysis_repository.save_analysis_result(
                db=db,
                request_id=saved_request.id,
                summary=None,
                root_cause=None,
                recommended_action=None,
                severity="UNKNOWN",
                model_name=None,
                prompt_version="system-prompt-v1",
                input_token_count=None,
                output_token_count=None
            )

            return LogAnalysisResponse(
                request_id=saved_request.id,
                status="INSUFFICIENT_CONTEXT",
                summary=None,
                root_cause=None,
                recommended_action=None,
                severity="UNKNOWN",
                referenced_chunks=[],
                model_name=None,
                prompt_version="v1",
                message="관련 운영 문서를 찾지 못해 LLM 분석을 수행하지 않았습니다."
            )

        #LLM에 넘길 context 구성
        similar_chunk_dicts = self.convert_similar_chunks_to_context(similar_chunks)

        #LLM 호출
        ai_result = generate_log_analysis(
            raw_log=request.raw_log,
            preprocessed_log=preprocessed_log,
            service_name=request.service_name,
            environment=request.environment,
            log_level=request.log_level,
            similar_chunks=similar_chunk_dicts
        )

        #분석 결과 저장
        self.log_analysis_repository.save_analysis_result(
            db=db,
            request_id=saved_request.id,
            summary=ai_result.get("summary"),
            root_cause=json.dumps(
                ai_result.get("possibleRootCauses"),
                ensure_ascii=False
            ),
            recommended_action=json.dumps(
                ai_result.get("safeActions"),
                ensure_ascii=False
            ),
            severity=ai_result.get("severity"),
            model_name="dummy-llm",
            prompt_version="system-prompt-v1",
            input_token_count=None,
            output_token_count=None
        )

        #요청 상태 변경 
        self.log_analysis_repository.update_analysis_request_status(
            db=db,
            request_id=saved_request.id,
            status="ANALYZED"
        )

        return LogAnalysisResponse(
            request_id=saved_request.id,
            status="ANALYZED",
            summary=ai_result.get("summary"),
            root_cause=ai_result.get("root_cause"),
            recommended_action=ai_result.get("recommended_action"),
            severity=ai_result.get("severity"),
            referenced_chunks=referenced_chunks,
            model_name=ai_result.get("model_name"),
            prompt_version=ai_result.get("prompt_version"),
            message=None
        )

    def convert_similar_chunks_to_context(self, rows) -> list[dict]:
        context = []

        for row in rows:
            context.append({
                "documentId": row.document_id,
                "chunkId": row.chunk_id,
                "title": row.title,
                "source": row.source,
                "content": row.content,
                "distance": float(row.distance) if row.distance is not None else None
            })

        return context