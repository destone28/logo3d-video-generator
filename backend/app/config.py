from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "3D Logo Video Generator"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # API
    API_V1_PREFIX: str = "/api/v1"
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    # Database
    DATABASE_URL: str = "postgresql://logo3d_user:logo3d_pass@localhost:5432/logo3d"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"

    # Storage (MinIO/S3)
    S3_ENDPOINT: str = "http://localhost:9000"
    S3_ACCESS_KEY: str = "minioadmin"
    S3_SECRET_KEY: str = "minioadmin"
    S3_BUCKET_NAME: str = "logo3d"
    S3_REGION: str = "us-east-1"

    # File Upload
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: set = {".png", ".jpg", ".jpeg", ".svg"}

    # Rendering
    BLENDER_PATH: str = "/usr/local/bin/blender"
    RENDER_OUTPUT_DIR: str = "/outputs"
    TEMP_DIR: str = "/tmp/logo3d"

    # Preview Settings
    PREVIEW_WIDTH: int = 854
    PREVIEW_HEIGHT: int = 480
    PREVIEW_FPS: int = 30
    PREVIEW_SAMPLES: int = 64

    # Final Render Settings
    RENDER_WIDTH_1080P: int = 1920
    RENDER_HEIGHT_1080P: int = 1080
    RENDER_WIDTH_4K: int = 3840
    RENDER_HEIGHT_4K: int = 2160
    RENDER_FPS: int = 30
    RENDER_SAMPLES_STANDARD: int = 256
    RENDER_SAMPLES_HIGH: int = 512

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
