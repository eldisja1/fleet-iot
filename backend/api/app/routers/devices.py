from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import Device
from ..schemas import DeviceResponse
from ..auth import authenticate

router = APIRouter(prefix="/devices", tags=["Devices"])


@router.get("/", response_model=List[DeviceResponse])
def get_devices(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    _=Depends(authenticate)
):
    return (
        db.query(Device)
        .offset(skip)
        .limit(limit)
        .all()
    )