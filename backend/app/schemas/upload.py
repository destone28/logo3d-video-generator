from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID
from typing import Optional

class UploadResponse(BaseModel):
    upload_id: UUID
    filename: str
    thumbnail_url: Optional[str] = None
    original_url: str
    width: int
    height: int
    file_size: int
    has_transparency: bool
    background_removed: bool
    created_at: datetime

    class Config:
        from_attributes = True

class BackgroundRemovalRequest(BaseModel):
    upload_id: UUID

class BackgroundRemovalResponse(BaseModel):
    upload_id: UUID
    processed_url: str
    success: bool
