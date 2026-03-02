from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from app.routers import devices_router, telemetry_router
from app.logging.logger import get_logger
import os

SERVICE_NAME = os.getenv("SERVICE_NAME", "api")
logger = get_logger(SERVICE_NAME)

app = FastAPI(
    title="Fleet IoT Enterprise API",
    version="2.0.0",
    description="Enterprise Fleet IoT API with validation and schema enforcement"
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


@app.get("/health", response_model=HealthResponse, tags=["System"])
def health():
    logger.info("Health check requested")
    return {"status": "ok"}


app.include_router(devices_router, tags=["Devices"])
app.include_router(telemetry_router, tags=["Telemetry"])