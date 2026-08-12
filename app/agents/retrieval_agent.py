from app.agents.base import BaseAgent
from app.models.agent import AgentRequest
from app.retrieval.service import RetrievalService


class RetrievalAgent(BaseAgent):
    """Retrieves enterprise knowledge relevant to a task."""

    name = "retrieval-agent"
    description = "Retrieves relevant knowledge for downstream agents."

    def __init__(
        self,
        retrieval_service: RetrievalService | None = None,
    ) -> None:
        super().__init__()

        self.retrieval_service = (
            retrieval_service or RetrievalService()
        )

    async def execute(self, request: AgentRequest) -> str:
        result = await self.retrieval_service.search(
            request.task
        )

        return result.model_dump_json(indent=2)