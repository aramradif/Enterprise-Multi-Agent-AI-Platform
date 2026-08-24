from pydantic import BaseModel, ConfigDict, Field


class SourceDocument(BaseModel):
    """A source document before chunking."""

    model_config = ConfigDict(extra="forbid")

    document_id: str
    content: str = Field(min_length=1)
    source: str
    metadata: dict[str, str] = Field(default_factory=dict)


class DocumentChunk(BaseModel):
    """A chunk prepared for embedding and retrieval."""

    model_config = ConfigDict(extra="forbid")

    chunk_id: str
    document_id: str
    content: str = Field(min_length=1)
    source: str
    chunk_index: int
    metadata: dict[str, str] = Field(default_factory=dict)