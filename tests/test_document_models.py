from app.models.document import DocumentChunk, SourceDocument


def test_source_document_creation() -> None:
    document = SourceDocument(
        document_id="financial-report-q1",
        content="Quarterly revenue increased by 12 percent.",
        source="q1-financial-report.txt",
    )

    assert document.document_id == "financial-report-q1"
    assert document.source == "q1-financial-report.txt"
    assert document.content


def test_document_chunk_creation() -> None:
    chunk = DocumentChunk(
        chunk_id="financial-report-q1-0",
        document_id="financial-report-q1",
        content="Quarterly revenue increased by 12 percent.",
        source="q1-financial-report.txt",
        chunk_index=0,
    )

    assert chunk.chunk_index == 0
    assert chunk.document_id == "financial-report-q1"
    assert chunk.content