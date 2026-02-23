import uuid
from datetime import datetime
from uuid import UUID
from typing import Optional

from pydantic import BaseModel, Field, constr, conint, confloat, ConfigDict


# =========================================================
# DEVICE SCHEMAS
# =========================================================

class DeviceResponse(BaseModel):
    id: UUID
    name: str
    status: str

    model_config = ConfigDict(from_attributes=True)


class DeviceCreate(BaseModel):
    name: constr(min_length=3, max_length=100)
    status: constr(min_length=3, max_length=50)


# =========================================================
# TELEMETRY SCHEMAS
# =========================================================

class TelemetryBase(BaseModel):
    device_id: UUID

    latitude: confloat(ge=-90.0, le=90.0)
    longitude: confloat(ge=-180.0, le=180.0)

    speed: confloat(ge=0.0, le=300.0)          # km/h realistic limit
    fuel_level: confloat(ge=0.0, le=100.0)     # percentage

    status: constr(min_length=3, max_length=50)


class TelemetryCreate(TelemetryBase):
    """
    Used for POST request validation.
    created_at optional (auto-generated if not provided)
    """
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)


class TelemetryResponse(TelemetryBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)