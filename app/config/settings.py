from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central application configuration loaded from environment variables."""

    app_name: str = "Enterprise Multi-Agent AI Platform"
    app_env: str = "development"
    app_debug: bool = True

    host: str = "127.0.0.1"
    port: int = 8000

    openai_api_key: str | None = None
    default_model: str = "gpt-4o-mini"
    embedding_model: str = "text-embedding-3-small"

    chroma_db_path: str = "./data/chromadb"
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Return one cached Settings instance for the application."""
    return Settings()