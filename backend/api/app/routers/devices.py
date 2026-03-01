from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import Device, Telemetry
from ..schemas import TelemetryResponse
from ..auth import authenticate

router = APIRouter(prefix="/devices", tags=["Devices"])


@router.get("/")
def get_devices(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    _=Depends(authenticate)
):
    offset = (page - 1) * limit

    devices = (
        db.query(Device)
        .offset(offset)
        .limit(limit)
        .all()
    )

    total = db.query(Device).count()

    return {
        "data": devices,
        "total": total,
        "page": page,
        "limit": limit
    }

@router.get("/{device_id}")
def get_device_detail(
    device_id: str,
    db: Session = Depends(get_db),
    _=Depends(authenticate)
):
    device = db.query(Device).filter(Device.id == device_id).first()

    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    return device

# TELEMETRY PER DEVICE + DEVICE NAME + PAGINATION 50
@router.get("/{device_id}/telemetry")
def get_device_telemetry(
    device_id: str, 
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    _=Depends(authenticate)
):
    device = db.query(Device).filter(Device.id == device_id).first()

    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    offset = (page - 1) * limit

    telemetry = (
        db.query(Telemetry)
        .filter(Telemetry.device_id == device_id)
        .offset(offset)
        .limit(limit)
        .all()
    )

    total = (
        db.query(Telemetry)
        .filter(Telemetry.device_id == device_id)
        .count()
    )

    return {
        "device_id": device.id,
        "device_name": device.name,
        "device_status": device.status, 
        "data": telemetry,
        "total": total,
        "page": page,
        "limit": limit
    }