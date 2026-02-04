from sqlalchemy import Column, Integer, String, DateTime, BigInteger, Text, Index
from sqlalchemy.sql import func
from app.core.database import Base


class FirewallLog(Base):
    """Firewall log model"""

    __tablename__ = "firewall_logs"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # Timestamp
    timestamp = Column(DateTime, nullable=False, index=True, default=func.now())

    # Network information
    source_ip = Column(String(45), nullable=False, index=True)  # IPv6 support
    source_port = Column(Integer, nullable=True)
    destination_ip = Column(String(45), nullable=False, index=True)
    destination_port = Column(Integer, nullable=True)

    # Protocol information
    protocol = Column(String(10), nullable=False, index=True)  # TCP/UDP/ICMP/etc
    action = Column(String(10), nullable=False, index=True)  # ALLOW/DENY/DROP

    # Direction
    direction = Column(String(10), nullable=False)  # INBOUND/OUTBOUND

    # Threat information
    severity = Column(String(20), nullable=False, default="INFO")  # INFO/LOW/MEDIUM/HIGH/CRITICAL
    threat_type = Column(String(50), nullable=True)  # malware/dos/scan/brute_force/etc

    # Statistics
    bytes_sent = Column(BigInteger, nullable=True, default=0)
    bytes_received = Column(BigInteger, nullable=True, default=0)
    packet_count = Column(Integer, nullable=True, default=0)

    # Metadata
    log_source = Column(String(100), nullable=True)  # firewall device identifier
    raw_log = Column(Text, nullable=True)  # original log entry
    description = Column(Text, nullable=True)

    # Composite indexes for common queries
    __table_args__ = (
        Index('idx_source_dest_ip', 'source_ip', 'destination_ip'),
        Index('idx_timestamp_action', 'timestamp', 'action'),
        Index('idx_timestamp_severity', 'timestamp', 'severity'),
    )

    def __repr__(self):
        return f"<FirewallLog(id={self.id}, timestamp={self.timestamp}, action={self.action})>"
