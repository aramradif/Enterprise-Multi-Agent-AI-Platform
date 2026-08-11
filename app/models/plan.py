from pydantic import BaseModel, ConfigDict


class PlanStep(BaseModel):
    """One step in an execution plan."""

    model_config = ConfigDict(extra="forbid")

    step_number: int
    title: str
    description: str
    assigned_agent: str


class ExecutionPlan(BaseModel):
    """Structured plan created by the Planning Agent."""

    model_config = ConfigDict(extra="forbid")

    objective: str
    steps: list[PlanStep]