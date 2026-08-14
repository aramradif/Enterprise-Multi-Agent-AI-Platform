import asyncio
import json
import pytest

from app.agents.planning_agent import PlanningAgent
from app.models.agent import AgentRequest, AgentStatus
from app.models.plan import ExecutionPlan

@pytest.mark.integration
def test_planning_agent_returns_valid_execution_plan() -> None:
    request = AgentRequest(
        task=(
            "Analyze our quarterly financial reports, "
            "identify risks, and prepare an executive summary."
        )
    )

    result = asyncio.run(PlanningAgent().run(request))

    assert result.agent_name == "planning-agent"
    assert result.status == AgentStatus.COMPLETED
    assert result.error is None
    assert result.output is not None
    assert result.execution_time_ms >= 0

    plan_data = json.loads(result.output)
    plan = ExecutionPlan.model_validate(plan_data)

    assert plan.objective
    assert len(plan.steps) > 0

    for step in plan.steps:
        assert step.step_number > 0
        assert step.title
        assert step.description
        assert step.assigned_agent