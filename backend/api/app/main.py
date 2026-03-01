from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from app.routers import devices_router, telemetry_router


app = FastAPI(
    title="Fleet IoT Enterprise API",
    version="2.0.0",
    description="Enterprise Fleet IoT API with validation and schema enforcement"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # nanti production kita restrict
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==============================
# Health Schema
# ==============================

class HealthResponse(BaseModel):
    status: str


# ==============================
# Health Endpoint
# ==============================

@app.get("/health", response_model=HealthResponse, tags=["System"])
def health():
    return {"status": "ok"}


# ==============================
# Routers
# ==============================

app.include_router(devices_router, tags=["Devices"])
app.include_router(telemetry_router, tags=["Telemetry"])