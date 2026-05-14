from sqlalchemy.orm import Session

# 유사 chunk 조회
def search_similar_chunks(
    db: Session,
    query_embedding: list[float],
    top_k: int=5
) -> list[dict]:
    """
        TODO:
        실제 구현에서는 pgvector similarity search를 수행한다.
        현재는 전체 흐름 테스트를 위해 빈 리스트를 반환한다.
    """

    return []
