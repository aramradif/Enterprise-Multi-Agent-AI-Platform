from time import perf_counter

from app.agents.base import BaseAgent
from app.agents.registry import AgentRegistry, build_default_registry
from app.models.agent import AgentRequest, AgentStatus
from app.models.plan import ExecutionPlan
from app.models.workflow import WorkflowResult, WorkflowStepResult


class SupervisorAgent(BaseAgent):
    """Coordinates specialized agents across the platform."""

    name = "supervisor-agent"
    description = "Coordinates planning and multi-agent execution."

    def __init__(
        self,
        registry: AgentRegistry | None = None,
    ) -> None:
        super().__init__()

        self.registry = registry or build_default_registry()

    async def execute(self, request: AgentRequest) -> str:
        workflow_start = perf_counter()

        # Step 1: Ask the Planning Agent to create a plan.
        planning_agent = self.registry.create(
            "planning-agent"
        )

        planning_result = await planning_agent.run(request)

        if planning_result.output is None:
            raise RuntimeError(
                planning_result.error
                or "Planning Agent returned no execution plan."
            )

        execution_plan = ExecutionPlan.model_validate_json(
            planning_result.output
        )

        workflow_steps: list[WorkflowStepResult] = []

        completed_steps = 0
        failed_steps = 0

        # Step 2: Execute currently supported plan steps.
        for plan_step in execution_plan.steps:
            if not self.registry.is_registered(
                plan_step.assigned_agent
            ):
                continue

            agent = self.registry.create(
                plan_step.assigned_agent
            )

            step_request = AgentRequest(
                task=plan_step.description
            )

            agent_result = await agent.run(
                step_request
            )

            workflow_steps.append(
                WorkflowStepResult(
                    step_number=plan_step.step_number,
                    title=plan_step.title,
                    assigned_agent=plan_step.assigned_agent,
                    result=agent_result,
                )
            )

            if agent_result.status == AgentStatus.COMPLETED:
                completed_steps += 1
            else:
                failed_steps += 1

        total_execution_time_ms = (
            perf_counter() - workflow_start
        ) * 1000

        workflow_result = WorkflowResult(
            objective=execution_plan.objective,
            steps=workflow_steps,
            completed_steps=completed_steps,
            failed_steps=failed_steps,
            total_execution_time_ms=round(
                total_execution_time_ms,
                2,
            ),
        )

        return workflow_result.model_dump_json(
            indent=2
        )