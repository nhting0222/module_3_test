import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.database import init_db, engine


async def main():
    """Initialize database - create all tables"""
    print("Initializing database...")
    print(f"Database URL: {engine.url}")

    try:
        await init_db()
        print("✓ Database initialized successfully!")
        print("✓ All tables created")
    except Exception as e:
        print(f"✗ Error initializing database: {e}")
        raise
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
