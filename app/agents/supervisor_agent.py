from app.agents.base import BaseAgent
from app.agents.registry import AgentRegistry, build_default_registry
from app.models.agent import AgentRequest


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
        planning_agent = self.registry.create(
            "planning-agent"
        )

        planning_result = await planning_agent.run(request)

        if planning_result.output is None:
            raise RuntimeError(
                planning_result.error
                or "Planning Agent returned no execution plan."
            )

        return planning_result.output