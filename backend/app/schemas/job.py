from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import Optional

class JobStatusResponse(BaseModel):
    job_id: UUID
    status: str
    progress: int
    estimated_remaining: Optional[int] = None
    result_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    error_message: Optional[str] = None
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class RenderHistoryItem(BaseModel):
    render_id: UUID
    created_at: datetime
    status: str
    config: dict
    thumbnail_url: Optional[str] = None
    video_url: Optional[str] = None
    duration: float
    resolution: str
    file_size: Optional[int] = None

    class Config:
        from_attributes = True
