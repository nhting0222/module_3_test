from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.core.database import get_db
from app.models.alert_rule import AlertRule
from app.schemas.alert_rule import AlertRuleCreate, AlertRuleResponse, AlertRuleUpdate

router = APIRouter()


@router.get("/", response_model=List[AlertRuleResponse])
async def get_alert_rules(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    enabled_only: bool = Query(False),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all alert rules with pagination
    Full implementation in Feature 2.4
    """
    query = select(AlertRule)

    if enabled_only:
        query = query.where(AlertRule.is_enabled == True)

    result = await db.execute(
        query.order_by(AlertRule.priority.desc()).offset(skip).limit(limit)
    )
    rules = result.scalars().all()
    return rules


@router.get("/{rule_id}", response_model=AlertRuleResponse)
async def get_alert_rule(rule_id: int, db: AsyncSession = Depends(get_db)):
    """Get a single alert rule by ID"""
    result = await db.execute(select(AlertRule).where(AlertRule.id == rule_id))
    rule = result.scalar_one_or_none()

    if not rule:
        raise HTTPException(status_code=404, detail="Alert rule not found")

    return rule


@router.post("/", response_model=AlertRuleResponse, status_code=201)
async def create_alert_rule(
    rule_data: AlertRuleCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new alert rule
    Full implementation in Feature 2.4
    """
    # Check if name already exists
    result = await db.execute(select(AlertRule).where(AlertRule.name == rule_data.name))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Alert rule name already exists")

    rule = AlertRule(**rule_data.model_dump())
    db.add(rule)
    await db.commit()
    await db.refresh(rule)
    return rule


@router.patch("/{rule_id}", response_model=AlertRuleResponse)
async def update_alert_rule(
    rule_id: int,
    rule_data: AlertRuleUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update an alert rule
    Full implementation in Feature 2.4
    """
    result = await db.execute(select(AlertRule).where(AlertRule.id == rule_id))
    rule = result.scalar_one_or_none()

    if not rule:
        raise HTTPException(status_code=404, detail="Alert rule not found")

    # Update fields
    update_data = rule_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(rule, field, value)

    await db.commit()
    await db.refresh(rule)
    return rule
