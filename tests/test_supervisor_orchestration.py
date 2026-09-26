import asyncio

from app.agents.supervisor_agent import SupervisorAgent
from app.models.agent import AgentRequest, AgentResult, AgentStatus
from app.models.workflow import WorkflowResult


class FakePlanningAgent:
    """Deterministic Planning Agent for orchestration testing."""

    async def run(
        self,
        request: AgentRequest,
    ) -> AgentResult:
        plan_json = """
        {
          "objective": "Analyze enterprise financial risks",
          "steps": [
            {
              "step_number": 1,
              "title": "Retrieve financial information",
              "description": "Retrieve relevant financial risk information.",
              "assigned_agent": "retrieval-agent"
            },
            {
              "step_number": 2,
              "title": "Analyze financial risks",
              "description": "Analyze the retrieved financial information.",
              "assigned_agent": "analysis-agent"
            }
          ]
        }
        """

        return AgentResult(
            agent_name="planning-agent",
            status=AgentStatus.COMPLETED,
            output=plan_json,
            execution_time_ms=10.0,
        )


class FakeRetrievalAgent:
    """Deterministic Retrieval Agent for orchestration testing."""

    async def run(
        self,
        request: AgentRequest,
    ) -> AgentResult:
        return AgentResult(
            agent_name="retrieval-agent",
            status=AgentStatus.COMPLETED,
            output=(
                "Liquidity risk and market volatility "
                "were identified."
            ),
            execution_time_ms=20.0,
        )

class FakeAnalysisAgent:
    """Deterministic Analysis Agent for orchestration testing."""

    async def run(
        self,
        request: AgentRequest,
    ) -> AgentResult:
        return AgentResult(
            agent_name="analysis-agent",
            status=AgentStatus.COMPLETED,
            output=(
                "The financial information indicates "
                "liquidity risk and market volatility."
            ),
            execution_time_ms=30.0,
        )
    
class FakeRegistry:
    """Minimal registry used to test Supervisor orchestration."""

    def is_registered(self, agent_name: str) -> bool:
        return agent_name in {
            "planning-agent",
            "retrieval-agent",
            "analysis-agent",
        }

    def create(self, agent_name: str):
        if agent_name == "planning-agent":
            return FakePlanningAgent()

        if agent_name == "retrieval-agent":
            return FakeRetrievalAgent()

        if agent_name == "analysis-agent":
            return FakeAnalysisAgent()

        raise KeyError(
            f"Agent not registered: {agent_name}"
        )


def test_supervisor_executes_retrieval_step() -> None:
    supervisor = SupervisorAgent(
        registry=FakeRegistry()
    )

    request = AgentRequest(
        task="Analyze enterprise financial risks."
    )

    result = asyncio.run(
        supervisor.run(request)
    )

    assert result.agent_name == "supervisor-agent"
    assert result.status == AgentStatus.COMPLETED
    assert result.error is None
    assert result.output is not None

    workflow = WorkflowResult.model_validate_json(
        result.output
    )

    assert workflow.objective == (
        "Analyze enterprise financial risks"
    )

    assert len(workflow.steps) == 2
    assert workflow.completed_steps == 2
    assert workflow.failed_steps == 0

    step = workflow.steps[0]

    assert step.step_number == 1
    assert step.title == "Retrieve financial information"
    assert step.assigned_agent == "retrieval-agent"

    assert step.result.agent_name == "retrieval-agent"
    assert step.result.status == AgentStatus.COMPLETED

    assert (
        "Liquidity risk"
        in step.result.output
    )

    analysis_step = workflow.steps[1]

    assert analysis_step.step_number == 2
    assert analysis_step.title == "Analyze financial risks"
    assert analysis_step.assigned_agent == "analysis-agent"

    assert analysis_step.result.agent_name == "analysis-agent"
    assert analysis_step.result.status == AgentStatus.COMPLETED

    assert (
        "liquidity risk"
        in analysis_step.result.output
)