from pydantic import BaseModel, ConfigDict


class RetrievedDocument(BaseModel):
    """One document returned by the retrieval layer."""

    model_config = ConfigDict(extra="forbid")

    content: str
    source: str
    score: float


class RetrievalResult(BaseModel):
    """Structured retrieval output."""

    model_config = ConfigDict(extra="forbid")

    query: str
    documents: list[RetrievedDocument]