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

     self.client: AsyncOpenAI | None = None

    async def execute(self, request: AgentRequest) -> str:
        if self.client is None:
            self.client = AsyncOpenAI(
                api_key=self.settings.openai_api_key
            )

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
"""

        response = await self.client.responses.parse(
            model=self.settings.default_model,
            input=prompt,
            text_format=ExecutionPlan,
        )

        for output in response.output:
            if output.type != "message":
                continue

            for item in output.content:
                if item.type != "output_text":
                    continue

                if item.parsed is None:
                    raise RuntimeError(
                        "Planning Agent did not return a parsed execution plan."
                    )

                plan = item.parsed

                return plan.model_dump_json(indent=2)

        raise RuntimeError(
            "Planning Agent returned no structured execution plan."
        )