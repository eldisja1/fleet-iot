from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Device, Telemetry
from ..auth import authenticate
from app.logging.logger import get_logger
import os

SERVICE_NAME = os.getenv("SERVICE_NAME", "api")
logger = get_logger(SERVICE_NAME)

router = APIRouter(prefix="/devices", tags=["Devices"])


@router.get("/")
def get_devices(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    _=Depends(authenticate)
):
    logger.info(f"Fetching devices page={page} limit={limit}")

    offset = (page - 1) * limit

    devices = db.query(Device).offset(offset).limit(limit).all()
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
    logger.info(f"Fetching device detail device_id={device_id}")

    device = db.query(Device).filter(Device.id == device_id).first()

    if not device:
        logger.warning(f"Device not found device_id={device_id}")
        raise HTTPException(status_code=404, detail="Device not found")

    return device


@router.get("/{device_id}/telemetry")
def get_device_telemetry(
    device_id: str,
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    _=Depends(authenticate)
):
    logger.info(f"Fetching telemetry device_id={device_id} page={page}")

    device = db.query(Device).filter(Device.id == device_id).first()

    if not device:
        logger.warning(f"Telemetry request for unknown device device_id={device_id}")
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