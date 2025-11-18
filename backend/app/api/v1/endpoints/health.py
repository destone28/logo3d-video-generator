from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ....database import get_db
from ....config import settings
import redis

router = APIRouter()

@router.get("/")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION
    }

@router.get("/detailed")
async def detailed_health_check(db: Session = Depends(get_db)):
    """Detailed health check with service status"""
    health_status = {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "services": {}
    }

    # Check database
    try:
        db.execute("SELECT 1")
        health_status["services"]["database"] = "healthy"
    except Exception as e:
        health_status["services"]["database"] = f"unhealthy: {str(e)}"
        health_status["status"] = "degraded"

    # Check Redis
    try:
        r = redis.from_url(settings.REDIS_URL)
        r.ping()
        health_status["services"]["redis"] = "healthy"
    except Exception as e:
        health_status["services"]["redis"] = f"unhealthy: {str(e)}"
        health_status["status"] = "degraded"

    # Check storage (MinIO/S3)
    try:
        from ....services.storage_service import storage_service
        # Simple bucket check
        storage_service.s3_client.head_bucket(Bucket=storage_service.bucket_name)
        health_status["services"]["storage"] = "healthy"
    except Exception as e:
        health_status["services"]["storage"] = f"unhealthy: {str(e)}"
        health_status["status"] = "degraded"

    return health_status
