from pydantic import BaseModel, Field


class PlanStep(BaseModel):
    """One step in an execution plan."""

    step_number: int
    title: str
    description: str
    assigned_agent: str


class ExecutionPlan(BaseModel):
    """Structured plan created by the Planning Agent."""

    objective: str
    steps: list[PlanStep] = Field(default_factory=list)