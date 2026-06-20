"""Application configuration — loaded from environment variables."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Coordinator settings loaded from env vars / .env file."""

    environment: str = "development"
    debug: bool = True

    # Database
    database_url: str = "postgresql+asyncpg://weave:weave@localhost:5432/weave"

    # Server
    host: str = "0.0.0.0"
    port: int = 8000

    # Coordinator
    max_concurrent_jobs: int = 100
    job_timeout_seconds: int = 300
    verification_sample_rate: float = 0.1  # Spot-check 10% of jobs via TOPLOC

    model_config = {"env_prefix": "WEAVE_", "env_file": ".env"}


settings = Settings()
