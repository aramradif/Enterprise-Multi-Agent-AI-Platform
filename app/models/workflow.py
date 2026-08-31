from pydantic import BaseModel, ConfigDict, Field

from app.models.agent import AgentResult


class WorkflowStepResult(BaseModel):
    """Result of one executed workflow step."""

    model_config = ConfigDict(extra="forbid")

    step_number: int
    title: str
    assigned_agent: str
    result: AgentResult


class WorkflowResult(BaseModel):
    """Complete result of a multi-agent workflow."""

    model_config = ConfigDict(extra="forbid")

    objective: str
    steps: list[WorkflowStepResult] = Field(default_factory=list)
    completed_steps: int = 0
    failed_steps: int = 0
    total_execution_time_ms: float = 0.0