#!/usr/bin/env python3
"""
Database initialization script
Creates all tables and runs initial migrations
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from app.database import engine, Base
from app.models import Upload, RenderJob
from app.config import settings

def init_db():
    """Initialize database"""
    print(f"Connecting to database: {settings.DATABASE_URL}")

    try:
        # Create all tables
        print("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("✓ Database tables created successfully")

        # Test connection
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            print("✓ Database connection successful")

        return True

    except Exception as e:
        print(f"✗ Database initialization failed: {e}")
        return False

if __name__ == "__main__":
    success = init_db()
    sys.exit(0 if success else 1)
