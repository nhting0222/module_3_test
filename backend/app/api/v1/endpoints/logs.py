from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List

from app.core.database import get_db
from app.models.firewall_log import FirewallLog
from app.schemas.firewall_log import FirewallLogCreate, FirewallLogResponse, FirewallLogUpdate

router = APIRouter()


@router.get("/", response_model=List[FirewallLogResponse])
async def get_logs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db)
):
    """
    Get firewall logs with pagination
    Full filtering implementation in Feature 2.3
    """
    result = await db.execute(
        select(FirewallLog)
        .order_by(FirewallLog.timestamp.desc())
        .offset(skip)
        .limit(limit)
    )
    logs = result.scalars().all()
    return logs


@router.get("/{log_id}", response_model=FirewallLogResponse)
async def get_log(log_id: int, db: AsyncSession = Depends(get_db)):
    """Get a single firewall log by ID"""
    result = await db.execute(select(FirewallLog).where(FirewallLog.id == log_id))
    log = result.scalar_one_or_none()

    if not log:
        raise HTTPException(status_code=404, detail="Log not found")

    return log


@router.post("/", response_model=FirewallLogResponse, status_code=201)
async def create_log(
    log_data: FirewallLogCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new firewall log
    Full implementation in Feature 2.2
    """
    log = FirewallLog(**log_data.model_dump())
    db.add(log)
    await db.commit()
    await db.refresh(log)
    return log


@router.get("/count/total")
async def get_log_count(db: AsyncSession = Depends(get_db)):
    """Get total log count"""
    result = await db.execute(select(func.count(FirewallLog.id)))
    count = result.scalar()
    return {"count": count}
