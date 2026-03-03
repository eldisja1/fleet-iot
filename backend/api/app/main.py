from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
import time
import os

from app.routers import devices_router, telemetry_router
from app.logging.logger import get_logger
from app.metrics import (
    http_requests_total,
    api_errors_total,
    http_request_duration_seconds
)

SERVICE_NAME = os.getenv("SERVICE_NAME", "api")
logger = get_logger(SERVICE_NAME)

app = FastAPI(
    title="Fleet IoT Enterprise API",
    version="3.0.0",
    description="Enterprise Fleet IoT API with monitoring and metrics"
)

logger.info("API service starting")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class HealthResponse(BaseModel):
    status: str


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    duration = time.time() - start_time

    endpoint = request.url.path
    method = request.method

    http_requests_total.labels(method=method, endpoint=endpoint).inc()
    http_request_duration_seconds.labels(endpoint=endpoint).observe(duration)

    if response.status_code >= 400:
        api_errors_total.inc()

    return response


@app.get("/health", response_model=HealthResponse, tags=["System"])
def health():
    logger.info("Health check requested")
    return {"status": "ok"}


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


app.include_router(devices_router, tags=["Devices"])
app.include_router(telemetry_router, tags=["Telemetry"])