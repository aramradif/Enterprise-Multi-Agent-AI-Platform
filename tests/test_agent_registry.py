import pytest

from app.agents.planning_agent import PlanningAgent
from app.agents.registry import AgentRegistry, build_default_registry


def test_default_registry_contains_planning_agent() -> None:
    registry = build_default_registry()

    assert "planning-agent" in registry.available_agents()


def test_registry_creates_planning_agent() -> None:
    registry = build_default_registry()

    agent = registry.create("planning-agent")

    assert isinstance(agent, PlanningAgent)


def test_registry_raises_for_unknown_agent() -> None:
    registry = AgentRegistry()

    with pytest.raises(KeyError):
        registry.create("unknown-agent")