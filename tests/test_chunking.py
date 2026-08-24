from app.models.document import SourceDocument
from app.retrieval.chunking import DocumentChunker


def test_chunker_splits_document() -> None:
    document = SourceDocument(
        document_id="doc-1",
        content="A" * 1200,
        source="sample.txt",
    )

    chunker = DocumentChunker(
        chunk_size=500,
        overlap=100,
    )

    chunks = chunker.chunk(document)

    assert len(chunks) == 3
    assert chunks[0].chunk_index == 0
    assert chunks[1].chunk_index == 1
    assert chunks[2].chunk_index == 2

    assert chunks[0].document_id == "doc-1"
    assert chunks[0].source == "sample.txt"


def test_chunker_preserves_overlap() -> None:
    document = SourceDocument(
        document_id="doc-2",
        content="0123456789",
        source="numbers.txt",
    )

    chunker = DocumentChunker(
        chunk_size=6,
        overlap=2,
    )

    chunks = chunker.chunk(document)

    assert chunks[0].content == "012345"
    assert chunks[1].content == "456789"


def test_chunker_rejects_invalid_configuration() -> None:
    try:
        DocumentChunker(
            chunk_size=100,
            overlap=100,
        )
    except ValueError as exc:
        assert "overlap" in str(exc)
    else:
        raise AssertionError("Expected ValueError")