import chromadb

from app.config.settings import get_settings
from app.models.document import DocumentChunk
from app.models.retrieval import RetrievedDocument
from app.retrieval.embeddings import EmbeddingService


class VectorStoreService:
    """Stores document chunks and performs semantic retrieval with ChromaDB."""

    def __init__(
        self,
        embedding_service: EmbeddingService | None = None,
    ) -> None:
        self.settings = get_settings()

        self.embedding_service = (
            embedding_service or EmbeddingService()
        )

        self.client = chromadb.PersistentClient(
            path=self.settings.chroma_db_path
        )

        self.collection = self.client.get_or_create_collection(
    name="enterprise_knowledge_cosine",
    configuration={
        "hnsw": {
            "space": "cosine"
        }
    },
)

    async def add_chunks(
        self,
        chunks: list[DocumentChunk],
    ) -> None:
        """Embed and store document chunks."""

        if not chunks:
            return

        texts = [
            chunk.content
            for chunk in chunks
        ]

        embeddings = await self.embedding_service.embed_texts(
            texts
        )

        self.collection.upsert(
            ids=[
                chunk.chunk_id
                for chunk in chunks
            ],
            documents=texts,
            embeddings=embeddings,
            metadatas=[
                {
                    "document_id": chunk.document_id,
                    "source": chunk.source,
                    "chunk_index": chunk.chunk_index,
                    **chunk.metadata,
                }
                for chunk in chunks
            ],
        )

    async def search(
        self,
        query: str,
        limit: int = 5,
    ) -> list[RetrievedDocument]:
        """Retrieve semantically relevant document chunks."""

        if not query.strip():
            raise ValueError("query cannot be empty")

        query_embedding = await self.embedding_service.embed_text(
            query
        )

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=limit,
        )

        retrieved: list[RetrievedDocument] = []

        documents = results.get("documents") or [[]]
        metadatas = results.get("metadatas") or [[]]
        distances = results.get("distances") or [[]]

        for document, metadata, distance in zip(
            documents[0],
            metadatas[0],
            distances[0],
        ):
            similarity_score = max(
                0.0,
                1.0 - float(distance),
            )

            retrieved.append(
                RetrievedDocument(
                    content=document,
                    source=str(
                        metadata.get(
                            "source",
                            "unknown",
                        )
                    ),
                    score=round(
                        similarity_score,
                        4,
                    ),
                )
            )

        return retrieved