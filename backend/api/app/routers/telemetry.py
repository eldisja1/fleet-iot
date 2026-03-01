from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
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


@router.get("/")
def get_telemetry(
    device_id: Optional[UUID] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    _=Depends(authenticate)
):
    if start_date and end_date and start_date > end_date:
        raise HTTPException(
            status_code=400,
            detail="start_date cannot be greater than end_date"
        )

    query = db.query(Telemetry)

    if device_id:
        query = query.filter(Telemetry.device_id == device_id)

    if start_date:
        query = query.filter(Telemetry.created_at >= start_date)

    if end_date:
        query = query.filter(Telemetry.created_at <= end_date)

    total = query.count()

    offset = (page - 1) * limit

    telemetry_data = (
        query
        .order_by(Telemetry.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return {
        "data": telemetry_data,
        "total": total,
        "page": page,
        "limit": limit
    }