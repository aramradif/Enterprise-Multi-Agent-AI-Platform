import asyncio
import json

import pytest

from app.agents.supervisor_agent import SupervisorAgent
from app.models.agent import AgentRequest, AgentStatus
from app.models.workflow import WorkflowResult


@pytest.mark.integration
def test_supervisor_agent_executes_workflow() -> None:
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

    workflow_data = json.loads(result.output)

    workflow = WorkflowResult.model_validate(
        workflow_data
    )

    assert workflow.objective
    assert len(workflow.steps) > 0

    assert (
        workflow.completed_steps
        + workflow.failed_steps
        == len(workflow.steps)
    )

    for step in workflow.steps:
        assert step.assigned_agent == "retrieval-agent"
        assert step.result.agent_name == "retrieval-agent"