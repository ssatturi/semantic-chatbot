# File: app/observability/tracing.py
from opentelemetry import trace
from opentelemetry.sdk.environment_variables import OTEL_EXPORTER_OTLP_LOGS_TIMEOUT
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
import os
from app.utils.config import settings


def setup_tracer(app, service_name="chatbot-api"):
    """
    Initialize OpenTelemetry tracer for distributed tracing.
    """
    trace.set_tracer_provider(
        TracerProvider(
            resource=Resource.create({"service.name": service_name})
        )
    )

    tracer_provider = trace.get_tracer_provider()

    # gRPC Exporter to otel-collector
    otlp_exporter = OTLPSpanExporter(
            endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "otel-collector:4317"),
            insecure=True
    )

    tracer_provider.add_span_processor(
        BatchSpanProcessor(otlp_exporter)
    )

    FastAPIInstrumentor.instrument_app(app)
    return trace.get_tracer(service_name)
