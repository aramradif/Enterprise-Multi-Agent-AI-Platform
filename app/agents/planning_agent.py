import json

from openai import AsyncOpenAI

from app.agents.base import BaseAgent
from app.models.agent import AgentRequest
from app.models.plan import ExecutionPlan


class PlanningAgent(BaseAgent):
    """Breaks complex tasks into structured multi-agent execution plans."""

    name = "planning-agent"
    description = "Creates structured execution plans for complex user tasks."

    def __init__(self) -> None:
        super().__init__()

        self.client = AsyncOpenAI(
            api_key=self.settings.openai_api_key
        )

    async def execute(self, request: AgentRequest) -> str:
        prompt = f"""
You are the Planning Agent in an enterprise multi-agent AI platform.

Your job is to break the user's request into a clear execution plan.

Available future agents:

- retrieval-agent
- research-agent
- analysis-agent
- report-agent
- quality-review-agent

Create a plan with:
1. The overall objective.
2. Ordered execution steps.
3. A title for each step.
4. A short description.
5. The agent responsible for the step.

User request:

{request.task}

Return valid JSON only in this format:

{{
  "objective": "...",
  "steps": [
    {{
      "step_number": 1,
      "title": "...",
      "description": "...",
      "assigned_agent": "..."
    }}
  ]
}}
"""

        response = await self.client.responses.create(
            model=self.settings.default_model,
            input=prompt,
        )

        raw_output = response.output_text

        if not raw_output or not raw_output.strip():
            raise RuntimeError(
                "Planning Agent received an empty response from the model."
            )

        clean_output = raw_output.strip()

        if clean_output.startswith("```json"):
            clean_output = clean_output[len("```json"):].strip()
        elif clean_output.startswith("```"):
            clean_output = clean_output[3:].strip()

        if clean_output.endswith("```"):
            clean_output = clean_output[:-3].strip()

        try:
            plan_data = json.loads(clean_output)
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                f"Planning Agent returned invalid JSON: {raw_output}"
            ) from exc

        plan = ExecutionPlan.model_validate(plan_data)

        return plan.model_dump_json(indent=2)