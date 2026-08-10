from collections.abc import Callable

from app.agents.base import BaseAgent
from app.agents.planning_agent import PlanningAgent


AgentFactory = Callable[[], BaseAgent]


class AgentRegistry:
    """Central registry for creating and retrieving platform agents."""

    def __init__(self) -> None:
        self._factories: dict[str, AgentFactory] = {}

    def register(
        self,
        agent_name: str,
        factory: AgentFactory,
    ) -> None:
        """Register an agent factory by name."""

        self._factories[agent_name] = factory

    def create(self, agent_name: str) -> BaseAgent:
        """Create a new agent instance by registered name."""

        factory = self._factories.get(agent_name)

        if factory is None:
            raise KeyError(
                f"Agent '{agent_name}' is not registered."
            )

        return factory()

    def available_agents(self) -> list[str]:
        """Return all registered agent names."""

        return sorted(self._factories.keys())


def build_default_registry() -> AgentRegistry:
    """Create the platform's default agent registry."""

    registry = AgentRegistry()

    registry.register(
        PlanningAgent.name,
        PlanningAgent,
    )

    return registry