from app.agents.analysis_agent import AnalysisAgent
from app.models.analysis import AnalysisResult


def test_analysis_agent_initializes_without_openai_client() -> None:
    agent = AnalysisAgent()

    assert agent.name == "analysis-agent"
    assert agent.client is None


def test_analysis_result_model() -> None:
    analysis = AnalysisResult(
        summary="Revenue increased while operating costs also increased.",
        key_findings=[
            "Revenue increased.",
            "Operating costs increased.",
        ],
        risks_or_gaps=[
            "Cost growth may reduce margins.",
        ],
        recommendations=[
            "Review the largest operating cost increases.",
        ],
    )

    assert analysis.summary
    assert len(analysis.key_findings) == 2
    assert len(analysis.risks_or_gaps) == 1
    assert len(analysis.recommendations) == 1