import logging
import os
from typing import Optional

import requests
from flask import Flask, jsonify, request
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import format_span_id, format_trace_id


SERVICE_NAME = os.getenv("OTEL_SERVICE_NAME", "simple-practice-app")
DEPLOYMENT_ENV = os.getenv("OTEL_DEPLOYMENT_ENV", "practice")
TRACE_ENDPOINT = os.getenv("OTEL_EXPORTER_OTLP_TRACES_ENDPOINT", "http://alloy:4318/v1/traces")
LOGS_ENDPOINT = os.getenv("OTEL_EXPORTER_OTLP_LOGS_ENDPOINT", "http://alloy:4318/v1/logs")


class TraceContextFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        span = trace.get_current_span()
        span_context = span.get_span_context()

        if span_context and span_context.is_valid:
            record.trace_id = format_trace_id(span_context.trace_id)
            record.span_id = format_span_id(span_context.span_id)
        else:
            record.trace_id = "-"
            record.span_id = "-"

        return True


resource = Resource.create(
    {
        "service.name": SERVICE_NAME,
        "deployment.environment": DEPLOYMENT_ENV,
        "service.version": "1.0.0",
    }
)

tracer_provider = TracerProvider(resource=resource)
tracer_provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=TRACE_ENDPOINT)))
trace.set_tracer_provider(tracer_provider)

logger_provider = LoggerProvider(resource=resource)
logger_provider.add_log_record_processor(BatchLogRecordProcessor(OTLPLogExporter(endpoint=LOGS_ENDPOINT)))

formatter = logging.Formatter(
    "%(asctime)s level=%(levelname)s service="
    + SERVICE_NAME
    + " trace_id=%(trace_id)s span_id=%(span_id)s message=%(message)s"
)

trace_filter = TraceContextFilter()

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
stream_handler.addFilter(trace_filter)

otel_handler = LoggingHandler(level=logging.INFO, logger_provider=logger_provider)
otel_handler.setFormatter(formatter)
otel_handler.addFilter(trace_filter)

root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
root_logger.handlers.clear()
root_logger.addHandler(stream_handler)
root_logger.addHandler(otel_handler)

logger = logging.getLogger(__name__)

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()


@app.get("/")
def index():
    logger.info("index requested")
    return jsonify({"message": "minimal lgtm lab is running"})


@app.get("/internal")
def internal():
    fail = request.args.get("fail", "false").lower() == "true"
    logger.info("internal endpoint called fail=%s", fail)

    if fail:
        logger.error("internal endpoint simulated failure")
        return jsonify({"status": "error", "message": "simulated failure"}), 500

    return jsonify({"status": "ok"})


def call_internal(fail: bool) -> requests.Response:
    url = f"http://127.0.0.1:8080/internal?fail={'true' if fail else 'false'}"
    logger.info("calling internal endpoint url=%s", url)
    return requests.get(url, timeout=2)


@app.get("/work")
def work():
    fail = request.args.get("fail", "false").lower() == "true"
    logger.info("start work fail=%s", fail)

    response: Optional[requests.Response] = None
    try:
        response = call_internal(fail)
        response.raise_for_status()
    except requests.RequestException as exc:
        status_code = response.status_code if response is not None else 500
        logger.exception("downstream call failed status=%s error=%s", status_code, exc)
        return (
            jsonify(
                {
                    "status": "error",
                    "fail": fail,
                    "message": "downstream call failed",
                    "status_code": status_code,
                }
            ),
            status_code,
        )

    logger.info("work completed status_code=%s", response.status_code)
    return jsonify({"status": "ok", "fail": fail, "downstream_status": response.status_code})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, threaded=True)
