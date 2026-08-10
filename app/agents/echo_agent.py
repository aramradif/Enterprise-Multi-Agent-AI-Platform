from app.agents.base import BaseAgent
from app.models.agent import AgentRequest


class EchoAgent(BaseAgent):
    """Temporary agent used to validate the agent framework."""

    name = "echo-agent"
    description = "Returns the submitted task as a test response."

    async def execute(self, request: AgentRequest) -> str:
        return f"Echo: {request.task}"