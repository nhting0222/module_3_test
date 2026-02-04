import asyncio
import sys
import random
from pathlib import Path
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal, engine
from app.core.security import get_password_hash
from app.models.user import User, UserRole
from app.models.firewall_log import FirewallLog
from app.models.alert_rule import AlertRule


async def create_users(db: AsyncSession):
    """Create test users"""
    users = [
        {
            "username": "admin",
            "email": "admin@example.com",
            "hashed_password": get_password_hash("admin123"),
            "role": UserRole.ADMIN,
            "is_active": True,
            "is_verified": True,
        },
        {
            "username": "operator",
            "email": "operator@example.com",
            "hashed_password": get_password_hash("operator123"),
            "role": UserRole.OPERATOR,
            "is_active": True,
            "is_verified": True,
        },
        {
            "username": "viewer",
            "email": "viewer@example.com",
            "hashed_password": get_password_hash("viewer123"),
            "role": UserRole.VIEWER,
            "is_active": True,
            "is_verified": True,
        },
    ]

    for user_data in users:
        user = User(**user_data)
        db.add(user)

    await db.commit()
    print(f"✓ Created {len(users)} users")


async def create_firewall_logs(db: AsyncSession):
    """Create random firewall logs"""
    protocols = ["TCP", "UDP", "ICMP", "HTTP", "HTTPS"]
    actions = ["ALLOW", "DENY", "DROP"]
    directions = ["INBOUND", "OUTBOUND"]
    severities = ["INFO", "LOW", "MEDIUM", "HIGH", "CRITICAL"]
    threat_types = ["malware", "dos", "scan", "brute_force", "suspicious", None]

    # Generate random IPs
    def random_ip():
        return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 255)}"

    logs = []
    base_time = datetime.utcnow() - timedelta(days=7)

    for i in range(500):
        log = FirewallLog(
            timestamp=base_time + timedelta(minutes=random.randint(0, 10080)),  # 7 days
            source_ip=random_ip(),
            source_port=random.randint(1024, 65535),
            destination_ip=random_ip(),
            destination_port=random.choice([80, 443, 22, 21, 3306, 8080, random.randint(1024, 65535)]),
            protocol=random.choice(protocols),
            action=random.choice(actions),
            direction=random.choice(directions),
            severity=random.choice(severities),
            threat_type=random.choice(threat_types),
            bytes_sent=random.randint(0, 1000000),
            bytes_received=random.randint(0, 1000000),
            packet_count=random.randint(1, 1000),
            log_source=f"firewall-{random.randint(1, 5)}",
            description=f"Firewall log entry {i+1}",
        )
        logs.append(log)

    db.add_all(logs)
    await db.commit()
    print(f"✓ Created {len(logs)} firewall logs")


async def create_alert_rules(db: AsyncSession):
    """Create sample alert rules"""
    rules = [
        {
            "name": "High Severity Alerts",
            "description": "Alert on high and critical severity events",
            "is_enabled": True,
            "conditions": {"severity": ["HIGH", "CRITICAL"]},
            "alert_type": "email",
            "alert_target": "security@example.com",
            "threshold_count": 5,
            "threshold_period": 300,
            "cooldown_period": 600,
            "priority": 9,
        },
        {
            "name": "Brute Force Detection",
            "description": "Detect potential brute force attacks",
            "is_enabled": True,
            "conditions": {"threat_type": "brute_force", "action": "DENY"},
            "alert_type": "webhook",
            "alert_target": "https://example.com/webhooks/alerts",
            "threshold_count": 10,
            "threshold_period": 60,
            "cooldown_period": 300,
            "priority": 8,
        },
        {
            "name": "Denied Connections",
            "description": "Monitor denied connection attempts",
            "is_enabled": False,
            "conditions": {"action": "DENY"},
            "alert_type": "email",
            "alert_target": "ops@example.com",
            "threshold_count": 50,
            "threshold_period": 600,
            "cooldown_period": 1800,
            "priority": 5,
        },
    ]

    for rule_data in rules:
        rule = AlertRule(**rule_data)
        db.add(rule)

    await db.commit()
    print(f"✓ Created {len(rules)} alert rules")


async def main():
    """Seed database with test data"""
    print("Seeding database with test data...")

    async with AsyncSessionLocal() as db:
        try:
            await create_users(db)
            await create_firewall_logs(db)
            await create_alert_rules(db)
            print("\n✓ Database seeded successfully!")
            print("\nTest Users:")
            print("  - admin / admin123 (ADMIN)")
            print("  - operator / operator123 (OPERATOR)")
            print("  - viewer / viewer123 (VIEWER)")
        except Exception as e:
            print(f"\n✗ Error seeding database: {e}")
            raise
        finally:
            await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
