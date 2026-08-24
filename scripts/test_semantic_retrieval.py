import asyncio

from app.models.document import SourceDocument
from app.retrieval.chunking import DocumentChunker
from app.retrieval.vector_store import VectorStoreService


async def main() -> None:
    document = SourceDocument(
        document_id="quarterly-financial-report",
        source="quarterly-financial-report.txt",
        content=(
            "The company reported strong quarterly financial performance. "
            "Revenue increased by 18 percent compared with the previous quarter. "
            "Operating expenses remained relatively stable. "
            "The company identified liquidity risk and market volatility "
            "as important financial risks for the upcoming quarter."
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

    print(f"Created {len(chunks)} chunks")

    vector_store = VectorStoreService()

    await vector_store.add_chunks(chunks)

    print("Chunks stored in ChromaDB")

    query = "What financial risks did the company identify?"

    print(f"\nQuery: {query}")

    results = await vector_store.search(
        query,
        limit=3,
    )

    print("\nSemantic Search Results:")

    for index, result in enumerate(
        results,
        start=1,
    ):
        print(f"\nResult {index}")
        print(f"Source: {result.source}")
        print(f"Score: {result.score}")
        print(f"Content: {result.content}")


if __name__ == "__main__":
    asyncio.run(main())