import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

from .db import init_db
from .logging_config import configure_logging
from .routes import public, auth, items
from .settings import settings


def create_app() -> FastAPI:
    logger = configure_logging("api-backend")

    resource = Resource(attributes={"service.name": "api-backend", "service.version": settings.api_version})
    trace.set_tracer_provider(TracerProvider(resource=resource))
    otlp_exporter = OTLPSpanExporter(endpoint=settings.otel_exporter_otlp_endpoint)
    span_processor = BatchSpanProcessor(otlp_exporter)
    trace.get_tracer_provider().add_span_processor(span_processor)

    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(public.router)
    app.include_router(auth.router)
    app.include_router(items.router)

    FastAPIInstrumentor.instrument_app(app)

    @app.on_event("startup")
    def on_startup() -> None:  # noqa: D401
        """Application startup hook."""

        logger.info("Starting up api-backend")
        init_db()

    return app


app = create_app()
