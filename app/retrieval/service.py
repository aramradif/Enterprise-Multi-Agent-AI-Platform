from app.models.retrieval import RetrievalResult
from app.retrieval.vector_store import VectorStoreService


class RetrievalService:
    """Retrieval abstraction for enterprise knowledge access."""

    def __init__(
        self,
        vector_store: VectorStoreService | None = None,
    ) -> None:
        self.vector_store = (
            vector_store or VectorStoreService()
        )

    async def search(
        self,
        query: str,
        limit: int = 5,
    ) -> RetrievalResult:
        """Retrieve semantically relevant enterprise knowledge."""

        documents = await self.vector_store.search(
            query=query,
            limit=limit,
        )

        return RetrievalResult(
            query=query,
            documents=documents,
        )