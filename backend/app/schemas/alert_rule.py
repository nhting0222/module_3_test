from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any


class AlertRuleBase(BaseModel):
    """Base schema for alert rule"""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    is_enabled: bool = True
    conditions: Dict[str, Any] = Field(..., description="JSON conditions for alert triggering")
    alert_type: str = Field(..., max_length=20, description="email/webhook/sms")
    alert_target: str = Field(..., max_length=255, description="Target address/URL/phone")
    threshold_count: int = Field(default=1, ge=1)
    threshold_period: int = Field(default=60, ge=1, description="Time period in seconds")
    cooldown_period: int = Field(default=300, ge=0, description="Cooldown in seconds")
    priority: int = Field(default=5, ge=1, le=10)


class AlertRuleCreate(AlertRuleBase):
    """Schema for creating an alert rule"""
    pass


class AlertRuleUpdate(BaseModel):
    """Schema for updating an alert rule"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    is_enabled: Optional[bool] = None
    conditions: Optional[Dict[str, Any]] = None
    alert_type: Optional[str] = Field(None, max_length=20)
    alert_target: Optional[str] = Field(None, max_length=255)
    threshold_count: Optional[int] = Field(None, ge=1)
    threshold_period: Optional[int] = Field(None, ge=1)
    cooldown_period: Optional[int] = Field(None, ge=0)
    priority: Optional[int] = Field(None, ge=1, le=10)


class AlertRuleResponse(AlertRuleBase):
    """Schema for alert rule response"""
    id: int
    last_triggered: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
