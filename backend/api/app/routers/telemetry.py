from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from uuid import UUID

from ..database import get_db
from ..models import Telemetry
from ..schemas import TelemetryResponse
from ..auth import authenticate

router = APIRouter(
    prefix="/telemetry",
    tags=["Telemetry"]
)


# ==========================
# GET ALL TELEMETRY
# ==========================
@router.get("/", response_model=List[TelemetryResponse])
def get_telemetry(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=500),
    db: Session = Depends(get_db),
    _=Depends(authenticate)
):
    # Date range validation
    if start_date and end_date:
        if start_date > end_date:
            raise HTTPException(
                status_code=400,
                detail="start_date cannot be greater than end_date"
            )

    query = db.query(Telemetry)

    if start_date:
        query = query.filter(Telemetry.created_at >= start_date)

    if end_date:
        query = query.filter(Telemetry.created_at <= end_date)

    telemetry_data = (
        query
        .order_by(Telemetry.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    return telemetry_data


# ==========================
# GET LAST 5 TELEMETRY BY DEVICE
# ==========================
@router.get("/{device_id}", response_model=List[TelemetryResponse])
def get_telemetry_by_device(
    device_id: UUID,
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    db: Session = Depends(get_db),
    _=Depends(authenticate)
):
    # Date validation
    if start_date and end_date:
        if start_date > end_date:
            raise HTTPException(
                status_code=400,
                detail="start_date cannot be greater than end_date"
            )

    query = db.query(Telemetry).filter(
        Telemetry.device_id == device_id
    )

    if start_date:
        query = query.filter(Telemetry.created_at >= start_date)

    if end_date:
        query = query.filter(Telemetry.created_at <= end_date)

    telemetry_data = (
        query
        .order_by(Telemetry.created_at.desc())
        .limit(5)
        .all()
    )

    if not telemetry_data:
        raise HTTPException(
            status_code=404,
            detail="No telemetry found for this device"
        )

    return telemetry_data