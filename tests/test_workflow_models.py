from app.models.agent import AgentResult, AgentStatus
from app.models.workflow import WorkflowResult, WorkflowStepResult


def test_workflow_step_result_creation() -> None:
    agent_result = AgentResult(
        agent_name="retrieval-agent",
        status=AgentStatus.COMPLETED,
        output="Retrieved enterprise documents.",
        execution_time_ms=125.5,
    )

    step = WorkflowStepResult(
        step_number=1,
        title="Retrieve enterprise knowledge",
        assigned_agent="retrieval-agent",
        result=agent_result,
    )

    assert step.step_number == 1
    assert step.assigned_agent == "retrieval-agent"
    assert step.result.status == AgentStatus.COMPLETED


def test_workflow_result_creation() -> None:
    workflow = WorkflowResult(
        objective="Analyze enterprise financial risks",
        completed_steps=1,
        failed_steps=0,
        total_execution_time_ms=125.5,
    )

    assert workflow.objective == "Analyze enterprise financial risks"
    assert workflow.completed_steps == 1
    assert workflow.failed_steps == 0
    assert workflow.steps == []