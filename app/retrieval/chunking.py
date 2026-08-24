from app.models.document import DocumentChunk, SourceDocument


class DocumentChunker:
    """Splits source documents into smaller retrieval chunks."""

    def __init__(
        self,
        chunk_size: int = 500,
        overlap: int = 100,
    ) -> None:
        if chunk_size <= 0:
            raise ValueError(
                "chunk_size must be greater than 0"
            )

        if overlap < 0:
            raise ValueError(
                "overlap cannot be negative"
            )

        if overlap >= chunk_size:
            raise ValueError(
                "overlap must be smaller than chunk_size"
            )

        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(
        self,
        document: SourceDocument,
    ) -> list[DocumentChunk]:
        """Split a document while avoiding word cuts when possible."""

        text = document.content.strip()

        if not text:
            return []

        chunks: list[DocumentChunk] = []

        start = 0
        chunk_index = 0

        while start < len(text):
            end = min(
                start + self.chunk_size,
                len(text),
            )

            # Prefer ending at whitespace when possible.
            # If there is no whitespace, keep the normal
            # character boundary so long words/data still chunk.
            if end < len(text):
                whitespace_position = text.rfind(
                    " ",
                    start,
                    end,
                )

                if whitespace_position > start:
                    end = whitespace_position

            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append(
                    DocumentChunk(
                        chunk_id=(
                            f"{document.document_id}-{chunk_index}"
                        ),
                        document_id=document.document_id,
                        content=chunk_text,
                        source=document.source,
                        chunk_index=chunk_index,
                        metadata=document.metadata.copy(),
                    )
                )

            if end >= len(text):
                break

            raw_next_start = max(
                0,
                end - self.overlap,
            )

            next_start = raw_next_start

            # Try to move the start forward to a word boundary,
            # but only when whitespace actually exists.
            if (
                next_start > 0
                and not text[next_start - 1].isspace()
            ):
                whitespace_position = text.find(
                    " ",
                    next_start,
                    end,
                )

                if whitespace_position != -1:
                    next_start = whitespace_position + 1

            start = next_start
            chunk_index += 1

        return chunks