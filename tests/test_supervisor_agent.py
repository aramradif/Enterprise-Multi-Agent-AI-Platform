import asyncio
import json
import pytest

from app.agents.supervisor_agent import SupervisorAgent
from app.models.agent import AgentRequest, AgentStatus
from app.models.plan import ExecutionPlan

@pytest.mark.integration
def test_supervisor_agent_returns_valid_plan() -> None:
    request = AgentRequest(
        task=(
            "Analyze our quarterly financial reports, "
            "identify risks, and prepare an executive summary."
        )
    )

    result = asyncio.run(
        SupervisorAgent().run(request)
    )

    assert result.agent_name == "supervisor-agent"
    assert result.status == AgentStatus.COMPLETED
    assert result.error is None
    assert result.output is not None

    plan_data = json.loads(result.output)
    plan = ExecutionPlan.model_validate(plan_data)

    assert plan.objective
    assert len(plan.steps) > 0