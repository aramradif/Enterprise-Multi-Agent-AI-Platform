import asyncio

from app.retrieval.embeddings import EmbeddingService


class FakeEmbedding:
    def __init__(self, values: list[float]) -> None:
        self.embedding = values


class FakeEmbeddingResponse:
    def __init__(self, embeddings: list[list[float]]) -> None:
        self.data = [
            FakeEmbedding(values)
            for values in embeddings
        ]


class FakeEmbeddingsAPI:
    async def create(
        self,
        model: str,
        input: str | list[str],
    ) -> FakeEmbeddingResponse:
        if isinstance(input, str):
            return FakeEmbeddingResponse(
                [[0.1, 0.2, 0.3]]
            )

        return FakeEmbeddingResponse(
            [
                [0.1, 0.2, 0.3]
                for _ in input
            ]
        )


class FakeOpenAIClient:
    def __init__(self) -> None:
        self.embeddings = FakeEmbeddingsAPI()


def test_embed_text_returns_embedding() -> None:
    service = EmbeddingService()
    service.client = FakeOpenAIClient()

    embedding = asyncio.run(
        service.embed_text("enterprise AI")
    )

    assert embedding == [0.1, 0.2, 0.3]


def test_embed_texts_returns_embeddings() -> None:
    service = EmbeddingService()
    service.client = FakeOpenAIClient()

    embeddings = asyncio.run(
        service.embed_texts(
            [
                "enterprise AI",
                "multi-agent systems",
            ]
        )
    )

    assert len(embeddings) == 2
    assert embeddings[0] == [0.1, 0.2, 0.3]


def test_embed_text_rejects_empty_text() -> None:
    service = EmbeddingService()

    try:
        asyncio.run(
            service.embed_text("   ")
        )
    except ValueError as exc:
        assert "empty" in str(exc)
    else:
        raise AssertionError(
            "Expected ValueError"
        )


def test_embed_texts_returns_empty_list() -> None:
    service = EmbeddingService()

    embeddings = asyncio.run(
        service.embed_texts([])
    )

    assert embeddings == []