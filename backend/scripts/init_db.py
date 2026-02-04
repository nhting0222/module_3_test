import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.database import init_db, engine
# Import models to register them with Base.metadata
from app.models import FirewallLog, User, AlertRule


async def main():
    """Initialize database - create all tables"""
    print("Initializing database...")
    print(f"Database URL: {engine.url}")

    try:
        await init_db()
        print("[OK] Database initialized successfully!")
        print("[OK] All tables created")
    except Exception as e:
        print(f"[ERROR] Error initializing database: {e}")
        raise
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
