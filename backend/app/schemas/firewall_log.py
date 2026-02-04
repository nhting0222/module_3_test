from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class FirewallLogBase(BaseModel):
    """Base schema for firewall log"""
    timestamp: datetime
    source_ip: str = Field(..., max_length=45)
    source_port: Optional[int] = None
    destination_ip: str = Field(..., max_length=45)
    destination_port: Optional[int] = None
    protocol: str = Field(..., max_length=10)
    action: str = Field(..., max_length=10)
    direction: str = Field(..., max_length=10)
    severity: str = Field(default="INFO", max_length=20)
    threat_type: Optional[str] = Field(None, max_length=50)
    bytes_sent: Optional[int] = Field(default=0, ge=0)
    bytes_received: Optional[int] = Field(default=0, ge=0)
    packet_count: Optional[int] = Field(default=0, ge=0)
    log_source: Optional[str] = Field(None, max_length=100)
    raw_log: Optional[str] = None
    description: Optional[str] = None


class FirewallLogCreate(FirewallLogBase):
    """Schema for creating a firewall log"""
    pass


class FirewallLogUpdate(BaseModel):
    """Schema for updating a firewall log"""
    severity: Optional[str] = Field(None, max_length=20)
    threat_type: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None


class FirewallLogResponse(FirewallLogBase):
    """Schema for firewall log response"""
    id: int

    class Config:
        from_attributes = True
