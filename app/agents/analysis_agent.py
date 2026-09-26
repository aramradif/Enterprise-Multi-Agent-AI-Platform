from openai import AsyncOpenAI

from app.agents.base import BaseAgent
from app.models.agent import AgentRequest
from app.models.analysis import AnalysisResult


class AnalysisAgent(BaseAgent):
    """Analyzes information and produces useful insights."""

    name = "analysis-agent"
    description = "Analyzes information and produces structured insights."

    def __init__(self) -> None:
        super().__init__()

        self.client: AsyncOpenAI | None = None

    async def execute(self, request: AgentRequest) -> str:
        if self.client is None:
            self.client = AsyncOpenAI(
                api_key=self.settings.openai_api_key
            )

        prompt = f"""
    You are the Analysis Agent in an enterprise multi-agent AI platform.

    Your job is to analyze the information provided in the task and produce
    clear, useful insights.

    Focus on:
    - key findings
    - important patterns or relationships
    - conclusions supported by the information
    - risks, gaps, or inconsistencies
    - actionable insights when appropriate

    Do not invent information that is not supported by the task.

    Task:

    {request.task}
    """

        response = await self.client.responses.parse(
            model=self.settings.default_model,
            input=prompt,
            text_format=AnalysisResult,
            )

        for output in response.output:
            if output.type != "message":
                continue

            for item in output.content:
                if item.type != "output_text":
                    continue

                if item.parsed is None:
                    raise RuntimeError(
                        "Analysis Agent did not return a parsed analysis."
                    )

                analysis = item.parsed

                return analysis.model_dump_json(indent=2)

        raise RuntimeError(
            "Analysis Agent returned no structured analysis."
        )
        
                