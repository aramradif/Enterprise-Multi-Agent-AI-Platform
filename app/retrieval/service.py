from app.models.retrieval import RetrievedDocument, RetrievalResult


class RetrievalService:
    """Retrieval abstraction for enterprise knowledge access."""

    async def search(self, query: str) -> RetrievalResult:
        """Return relevant documents for a query.

        This initial implementation is intentionally local.
        ChromaDB integration will replace it later.
        """

        documents = [
            RetrievedDocument(
                content=(
                    "Quarterly financial reports contain revenue, "
                    "operating expenses, profit, cash flow, and risk disclosures."
                ),
                source="sample-financial-report",
                score=0.95,
            ),
            RetrievedDocument(
                content=(
                    "Risk analysis should consider liquidity, revenue concentration, "
                    "operating margin changes, and external market conditions."
                ),
                source="sample-risk-guidance",
                score=0.90,
            ),
        ]

        return RetrievalResult(
            query=query,
            documents=documents,
        )