from typing import List

class MockEmbeddingClient:
    async def create_embedding(self, text: str) -> List[float]:
        return [0.01] * 1536
    # ex) [0.01, 0.01, 0.01, 0.01, ...]