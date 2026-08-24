import asyncio

from app.models.document import DocumentChunk
from app.retrieval.vector_store import VectorStoreService


class FakeEmbeddingService:
    """Provides deterministic embeddings without calling OpenAI."""

    async def embed_text(
        self,
        text: str,
    ) -> list[float]:
        return [0.1, 0.2, 0.3]

    async def embed_texts(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        return [
            [0.1, 0.2, 0.3]
            for _ in texts
        ]


def test_vector_store_adds_and_retrieves_chunk(
    tmp_path,
) -> None:
    service = VectorStoreService(
        embedding_service=FakeEmbeddingService()
    )

    # Use an isolated Chroma database for this test.
    import chromadb

    service.client = chromadb.PersistentClient(
        path=str(tmp_path / "chroma")
    )

    service.collection = (
        service.client.get_or_create_collection(
            name="test_enterprise_knowledge"
        )
    )

    chunk = DocumentChunk(
        chunk_id="financial-report-0",
        document_id="financial-report",
        content=(
            "Quarterly revenue increased by 18 percent "
            "while operating expenses remained stable."
        ),
        source="financial-report.txt",
        chunk_index=0,
    )

    asyncio.run(
        service.add_chunks([chunk])
    )

    results = asyncio.run(
        service.search(
            "How did quarterly revenue change?",
            limit=1,
        )
    )

    assert len(results) == 1
    assert results[0].source == "financial-report.txt"
    assert "revenue" in results[0].content.lower()


def test_vector_store_accepts_empty_chunk_list(
    tmp_path,
) -> None:
    service = VectorStoreService(
        embedding_service=FakeEmbeddingService()
    )

    asyncio.run(
        service.add_chunks([])
    )


def test_vector_store_rejects_empty_query(
    tmp_path,
) -> None:
    service = VectorStoreService(
        embedding_service=FakeEmbeddingService()
    )

    try:
        asyncio.run(
            service.search("   ")
        )
    except ValueError as exc:
        assert "empty" in str(exc)
    else:
        raise AssertionError(
            "Expected ValueError"
        )