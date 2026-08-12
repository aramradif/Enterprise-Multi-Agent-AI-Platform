import asyncio
import json

from app.agents.retrieval_agent import RetrievalAgent
from app.models.agent import AgentRequest, AgentStatus


def test_retrieval_agent_returns_documents() -> None:
    request = AgentRequest(
        task="Analyze quarterly financial risks"
    )

    result = asyncio.run(
        RetrievalAgent().run(request)
    )

    assert result.agent_name == "retrieval-agent"
    assert result.status == AgentStatus.COMPLETED
    assert result.error is None
    assert result.output is not None

    retrieval_data = json.loads(result.output)

    assert retrieval_data["query"] == request.task
    assert len(retrieval_data["documents"]) == 2
    assert retrieval_data["documents"][0]["source"] == "sample-financial-report"
    assert retrieval_data["documents"][0]["score"] == 0.95