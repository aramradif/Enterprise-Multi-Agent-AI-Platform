from openai import AsyncOpenAI

from app.config.settings import get_settings


class EmbeddingService:
    """Creates vector embeddings for document chunks and search queries."""

    def __init__(self) -> None:
        self.settings = get_settings()
        self.client: AsyncOpenAI | None = None

    def _get_client(self) -> AsyncOpenAI:
        """Create the OpenAI client only when it is actually needed."""

        if self.client is None:
            self.client = AsyncOpenAI(
                api_key=self.settings.openai_api_key
            )

        return self.client

    async def embed_text(self, text: str) -> list[float]:
        """Create an embedding for a single text value."""

        if not text.strip():
            raise ValueError("text cannot be empty")

        client = self._get_client()

        response = await client.embeddings.create(
            model=self.settings.embedding_model,
            input=text,
        )

        return response.data[0].embedding

    async def embed_texts(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """Create embeddings for multiple text values."""

        if not texts:
            return []

        if any(not text.strip() for text in texts):
            raise ValueError("texts cannot contain empty values")

        client = self._get_client()

        response = await client.embeddings.create(
            model=self.settings.embedding_model,
            input=texts,
        )

        return [item.embedding for item in response.data]