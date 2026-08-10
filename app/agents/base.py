import logging
from abc import ABC, abstractmethod
from time import perf_counter

from app.config.settings import Settings, get_settings
from app.models.agent import AgentRequest, AgentResult, AgentStatus


class BaseAgent(ABC):
    """Reusable foundation inherited by every specialized agent."""

    name = "base-agent"
    description = "Base implementation for platform agents."

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self.logger = logging.getLogger(self.name)

    async def run(self, request: AgentRequest) -> AgentResult:
        """Execute the agent with standardized timing and error handling."""

        started_at = perf_counter()

        self.logger.info(
            "Agent '%s' started task for session '%s'.",
            self.name,
            request.session_id,
        )

        try:
            output = await self.execute(request)

            execution_time_ms = (perf_counter() - started_at) * 1000

            self.logger.info(
                "Agent '%s' completed in %.2f ms.",
                self.name,
                execution_time_ms,
            )

            return AgentResult(
                agent_name=self.name,
                status=AgentStatus.COMPLETED,
                output=output,
                execution_time_ms=round(execution_time_ms, 2),
            )

        except Exception as exc:
            execution_time_ms = (perf_counter() - started_at) * 1000

            self.logger.exception(
                "Agent '%s' failed while processing session '%s'.",
                self.name,
                request.session_id,
            )

            return AgentResult(
                agent_name=self.name,
                status=AgentStatus.FAILED,
                error=str(exc),
                execution_time_ms=round(execution_time_ms, 2),
            )

    @abstractmethod
    async def execute(self, request: AgentRequest) -> str:
        """Perform the specialized work implemented by a child agent."""

        raise NotImplementedError