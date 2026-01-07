import os
from dataclasses import dataclass


@dataclass
class Settings:
    api_version: str = os.getenv("API_VERSION", "dev")

    jwt_secret: str = os.getenv("JWT_SECRET", "change-me-in-prod")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("JWT_EXPIRE_MINUTES", "30"))

    demo_username: str = os.getenv("DEMO_USERNAME", "admin")
    demo_password: str = os.getenv("DEMO_PASSWORD", "admin")

    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql://apibackend:apibackend123@127.0.0.1:5432/apibackend",
    )

    redis_url: str = os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0")

    otel_exporter_otlp_endpoint: str = os.getenv(
        "OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4318/v1/traces"
    )


settings = Settings()
