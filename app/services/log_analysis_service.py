import logging, json, time

from sqlalchemy.orm import Session

from app.schemas.log_analysis_schema import (
    LogAnalysisRequest, 
    LogAnalysisResponse,
    SimilarChunkResponse,
    LogAnalysisDetailResponse
)
from app.repositories.log_analysis_repository import LogAnalysisRepository
from app.repositories.log_analysis_result_repository import LogAnalysisResultRepository
from app.repositories.log_analysis_reference_repository import LogAnalysisReferenceRepository
from app.repositories.document_search_repository import DocumentSearchRepository

from app.prompts.log_analysis_prompt import (
    create_system_prompt,
    create_user_prompt,
)

from app.utils.embedding import create_embedding
from app.utils.llm_client import call_llm


log = logging.getLogger(__name__)


class LogAnalysisService:

    def __init__(self):
        self.request_repository = LogAnalysisRepository()
        self.result_repository = LogAnalysisResultRepository()
        self.reference_repository =  LogAnalysisReferenceRepository()
        self.document_search_repository = DocumentSearchRepository()

    def analyze_log(
            self, 
            request: LogAnalysisRequest, 
            db:Session
    ) -> LogAnalysisResponse:
        #분석 요청 저장
        saved_request = self.request_repository.save_analysis_request(
            db=db,
            request = request,
            status="PENDING"
        )

        try:
            start_time = time.time()

            #embedding
            query_embedding = create_embedding(request.raw_log) 

            #관련 운영 문서 chunk검색
            similar_chunks = self.document_search_repository.search_similar_chunks( 
                db=db,
                query_embedding=query_embedding,
                top_k=request.top_k,
                threshold=request.threshold
            )

            #dict 목록으로 변환
            similar_chunk_dicts = self.convert_similar_chunks_to_dicts(similar_chunks)

            #참고 문서가 없을경우
            if len(similar_chunk_dicts) == 0:
                self.request_repository.update_analysis_request_status(
                    db=db,
                    request_id=saved_request.id,
                    status="COMPLETED"
                )

                return LogAnalysisResponse(
                    request_id=saved_request.id,
                    result_id=None,
                    status="INSUFFICIENT_CONTEXT",
                    summary=None,
                    root_cause=None,
                    recommended_action=None,
                    severity="UNKNOWN",
                    referenced_chunks=[],
                    model_name=None,
                    prompt_version=None,
                    input_token_count=None,
                    output_token_count=None,
                    total_tokens=None,
                    latency_ms=None,
                    message="분석에 참고할 수 있는 운영 문서를 찾지 못했습니다."
                )
            
            # prompt system, user
            system_prompt = create_system_prompt
            user_prompt = create_user_prompt(
                request=request,
                similar_chunks=similar_chunk_dicts
            )

            # Open AI call
            llm_response_text = call_llm(
                system_prompt=system_prompt,
                user_prompt=user_prompt
            )

            llm_response = json.loads(llm_response_text)

            end_time = time.time()
            latency_ms = int((end_time - start_time) * 1000)

            summary = llm_response.get("summary")
            root_cause = self.extract_root_cause(llm_response)
            recommended_action = self.extract_recommended_action(llm_response)
            severity = llm_response.get("severity", "UNKNOWN")

            model_name = "dummy-llm"
            prompt_version = "v1"

            input_token_count = None
            output_token_count = None
            total_tokens = None

            saved_result = self.result_repository.save_result(
                db=db,
                request_id=saved_request.id,
                summary=summary,
                root_cause=root_cause,
                recommended_action=recommended_action,
                severity=severity,
                model_name=model_name,
                prompt_version=prompt_version,
                input_token_count=input_token_count,
                output_token_count=output_token_count,
                total_tokens=total_tokens,
                latency_ms=latency_ms
            )

            self.reference_repository.save_references(
                db=db,
                result_id=saved_result.id,
                similar_chunks=similar_chunk_dicts
            )

            self.request_repository.update_analysis_request_status(
                db=db,
                request_id=saved_request.id,
                status="COMPLETED"
            )

            return LogAnalysisResponse(
                request_id=saved_request.id,
                result_id=saved_result.id,
                status="ANALYZED",
                summary=saved_result.summary,
                root_cause=saved_result.root_cause,
                recommended_action=saved_result.recommended_action,
                severity=saved_result.severity,
                referenced_chunks=[
                    SimilarChunkResponse(
                        chunk_id=chunk["chunk_id"],
                        document_id=chunk["document_id"],
                        title=chunk.get("title"),
                        content=chunk["content"],
                        distance=chunk.get("distance"),
                        similarity_score=chunk.get("similarity_score"),
                        rank_order=chunk.get("rank_order")
                    )
                    for chunk in similar_chunk_dicts
                ],
                model_name=saved_result.model_name,
                prompt_version=saved_result.prompt_version,
                input_token_count=saved_result.input_token_count,
                output_token_count=saved_result.output_token_count,
                total_tokens=saved_result.total_tokens,
                latency_ms=saved_result.latency_ms,
                message="로그 분석이 완료되었습니다."
            )
        
        except Exception as e:
                self.request_repository.update_analysis_request_status(
                    db=db,
                    request_id=saved_request.id,
                    status="FAILED"
                )
                raise e


    #조회
    def get_analysis_detail(
        self,
        analysis_id: int,
        db:Session
    ) -> LogAnalysisDetailResponse:
        #요청 정보 조회
        analysis_request = self.request_repository.get_analysis_request_by_id(
            db=db,
            request_id=analysis_id
        )

        if analysis_request is None:
            raise ValueError("분석 요청을 찾을 수 없습니다.")
        
        #분석 결과 조회
        result = self.request_repository.get_analysis_result_by_request_id(
            db=db,
            request_id=analysis_id
        )

        referenced_chunks = []

        if result is not None:
            #chunks 조회
            references = self.reference_repository.find_by_result_id(
                db=db,
                result_id = result.id
            )

            referenced_chunks = [
                SimilarChunkResponse(
                    chunk_id=row.chunk_id,
                    document_id=row.document_id,
                    title=row.title,
                    content=row.content,
                    distance=row.distance,
                    similarity_score=row.similarity_score,
                    rank_order=row.rank_order
                )
                for row in references
            ]

        return LogAnalysisDetailResponse(
            request=analysis_request,
            result=result,
            referenced_chunks=referenced_chunks
        )


    #DocumentSearchRepository에서 조회한 row를 dict 목록으로 변환
    def convert_similar_chunks_to_dicts(self, similar_chunks) -> list[dict]:
        result = []

        for index, row in enumerate(similar_chunks):
            chunk_id = self.get_row_value(row, "chunk_id")
            document_id = self.get_row_value(row, "document_id")
            title = self.get_row_value(row, "title")
            content = self.get_row_value(row, "content")
            distance = self.get_row_value(row, "distance")
            similarity_score = self.get_row_value(row, "similarity_score")

            if similarity_score is None and distance is not None:
                similarity_score = 1 - distance
            
            result.append({
                "chunk_id": chunk_id,
                "document_id": document_id,
                "title": title,
                "content": content,
                "distance": distance,
                "similarity_score": similarity_score,
                "rank_order": index + 1
            })

        return result

    #SQLAlchemy row, dict, named tuple 형태를 모두 처리하기 위한 helper
    def get_row_value(self, row, key: str): 
        if isinstance(row, dict):
            return row.get(key)
        
        if hasattr(row, key):
            return getattr(row, key)
    
        if hasattr(row, "_mapping"):
            return row._mapping.get(key)
        
        return None
    
    # LLM 응답의 possibleRootCauses 배열에서 첫 번째 원인을 root_cause로 사용한다.
    def extract_root_cause(self, llm_response: dict) -> str | None:
        possible_root_causes = llm_response.get("possibleRootCauses", [])

        if not possible_root_causes:
            return None

        first_cause = possible_root_causes[0]

        return first_cause.get("cause")


    def extract_recommended_action(self, llm_response: dict) -> str | None:
        safe_actions = llm_response.get("safeActions", [])

        if len(safe_actions) == 0:
            return None

        actions = []

        for item in safe_actions:
            action = item.get("action")

            if action:
                actions.append(action)

        return "\n".join(actions)
