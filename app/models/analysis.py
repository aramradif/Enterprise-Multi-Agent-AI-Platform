from pydantic import BaseModel, Field


class AnalysisResult(BaseModel):
    """Structured output produced by the Analysis Agent."""

    summary: str
    key_findings: list[str] = Field(default_factory=list)
    risks_or_gaps: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)