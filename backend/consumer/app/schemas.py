from datetime import datetime
from uuid import UUID
from typing import Optional

from pydantic import BaseModel, Field, confloat, constr, ConfigDict


class TelemetryMQTT(BaseModel):
    # device_id tidak diperlukan karena sudah diambil dari topic MQTT

    latitude: confloat(ge=-90.0, le=90.0)
    longitude: confloat(ge=-180.0, le=180.0)

    speed: confloat(ge=0.0, le=300.0)
    fuel_level: confloat(ge=0.0, le=100.0)

    status: constr(min_length=3, max_length=50)

    # created_at tidak wajib karena DB sudah DEFAULT CURRENT_TIMESTAMP
    created_at: Optional[datetime] = None

    model_config = ConfigDict(extra="ignore")  # agar timestamp dari simulator tidak error