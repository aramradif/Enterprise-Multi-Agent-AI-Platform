import asyncio

from app.agents.retrieval_agent import RetrievalAgent
from app.models.agent import AgentRequest, AgentStatus
from app.models.retrieval import RetrievedDocument, RetrievalResult
from app.retrieval.service import RetrievalService


class FakeVectorStore:
    """Deterministic vector store used for unit testing."""

    async def search(
        self,
        query: str,
        limit: int = 5,
    ) -> list[RetrievedDocument]:
        return [
            RetrievedDocument(
                content=(
                    "The company identified liquidity risk "
                    "and market volatility."
                ),
                source="financial-report.txt",
                score=0.88,
            )
        ]


def test_retrieval_agent_returns_semantic_results() -> None:
    retrieval_service = RetrievalService(
        vector_store=FakeVectorStore()
    )

    agent = RetrievalAgent(
        retrieval_service=retrieval_service
    )

    request = AgentRequest(
        task="What financial risks were identified?"
    )

    result = asyncio.run(
        agent.run(request)
    )

    assert result.agent_name == "retrieval-agent"
    assert result.status == AgentStatus.COMPLETED
    assert result.error is None
    assert result.output is not None

    retrieval_result = RetrievalResult.model_validate_json(
        result.output
    )

    assert retrieval_result.query == request.task
    assert len(retrieval_result.documents) == 1
    assert (
        retrieval_result.documents[0].source
        == "financial-report.txt"
    )
    assert (
        "liquidity risk"
        in retrieval_result.documents[0].content.lower()
    )