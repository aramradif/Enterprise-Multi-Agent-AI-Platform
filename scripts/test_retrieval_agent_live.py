import asyncio

from app.agents.retrieval_agent import RetrievalAgent
from app.models.agent import AgentRequest
from app.models.document import SourceDocument
from app.retrieval.chunking import DocumentChunker
from app.retrieval.vector_store import VectorStoreService


async def main() -> None:
    document = SourceDocument(
        document_id="live-financial-report",
        source="live-financial-report.txt",
        content=(
            "The company reported strong quarterly financial performance. "
            "Revenue increased by 18 percent compared with the previous quarter. "
            "Operating expenses remained stable. "
            "The company identified liquidity risk and market volatility "
            "as the primary financial risks for the upcoming quarter."
        ),
        metadata={
            "department": "finance",
            "document_type": "financial-report",
        },
    )

    chunker = DocumentChunker(
        chunk_size=150,
        overlap=30,
    )

    chunks = chunker.chunk(document)

    vector_store = VectorStoreService()

    await vector_store.add_chunks(chunks)

    print(f"Stored {len(chunks)} chunks in ChromaDB")

    agent = RetrievalAgent()

    request = AgentRequest(
        task="What financial risks did the company identify?"
    )

    result = await agent.run(request)

    print("\nRetrieval Agent Result:")
    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    asyncio.run(main())