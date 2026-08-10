from fastapi import FastAPI

from app.config.settings import get_settings


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description=(
        "Production-ready Enterprise Multi-Agent AI Platform "
        "for agent orchestration, retrieval, analysis, reporting, "
        "quality review, and human approval workflows."
    ),
)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "message": f"{settings.app_name} is running",
        "environment": settings.app_env,
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": settings.app_name,
        "version": "1.0.0",
        "environment": settings.app_env,
    }