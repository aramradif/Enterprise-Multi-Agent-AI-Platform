import asyncio

from app.agents.echo_agent import EchoAgent
from app.models.agent import AgentRequest, AgentStatus


def test_echo_agent_returns_standardized_result() -> None:
    request = AgentRequest(task="Test the enterprise agent framework")

    result = asyncio.run(EchoAgent().run(request))

    assert result.agent_name == "echo-agent"
    assert result.status == AgentStatus.COMPLETED
    assert result.output == "Echo: Test the enterprise agent framework"
    assert result.error is None
    assert result.execution_time_ms >= 0