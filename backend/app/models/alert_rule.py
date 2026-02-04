from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON
from sqlalchemy.sql import func
from app.core.database import Base


class AlertRule(Base):
    """Alert rule model for monitoring firewall logs"""

    __tablename__ = "alert_rules"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # Basic information
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)

    # Status
    is_enabled = Column(Boolean, default=True, nullable=False, index=True)

    # Rule conditions (flexible JSON structure)
    # Example: {"source_ip": "192.168.1.100", "action": "DENY", "severity": ["HIGH", "CRITICAL"]}
    conditions = Column(JSON, nullable=False)

    # Alert configuration
    alert_type = Column(String(20), nullable=False)  # email/webhook/sms
    alert_target = Column(String(255), nullable=False)  # email address, webhook URL, phone number

    # Threshold settings
    threshold_count = Column(Integer, default=1, nullable=False)  # Number of occurrences
    threshold_period = Column(Integer, default=60, nullable=False)  # Time period in seconds

    # Cooldown to prevent duplicate alerts
    cooldown_period = Column(Integer, default=300, nullable=False)  # Seconds before re-alerting
    last_triggered = Column(DateTime, nullable=True)

    # Priority (1-10, higher is more important)
    priority = Column(Integer, default=5, nullable=False)

    # Timestamps
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<AlertRule(id={self.id}, name={self.name}, enabled={self.is_enabled})>"
