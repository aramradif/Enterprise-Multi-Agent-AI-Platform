from enum import StrEnum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


class AgentStatus(StrEnum):
    """Possible execution states for an agent."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class AgentRequest(BaseModel):
    """Standard input accepted by every agent."""

    task: str = Field(min_length=1)
    session_id: str = Field(default_factory=lambda: str(uuid4()))
    context: dict[str, Any] = Field(default_factory=dict)


class AgentResult(BaseModel):
    """Standard response returned by every agent."""

    agent_name: str
    status: AgentStatus
    output: str | None = None
    error: str | None = None
    execution_time_ms: float = 0.0
    metadata: dict[str, Any] = Field(default_factory=dict)