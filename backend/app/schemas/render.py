from pydantic import BaseModel, Field
from typing import Optional, Literal
from uuid import UUID

class BackgroundConfig(BaseModel):
    type: Literal["solid", "gradient", "transparent", "hdri"] = "solid"
    color: Optional[str] = "#ffffff"
    gradient_start: Optional[str] = None
    gradient_end: Optional[str] = None
    hdri_name: Optional[str] = None

class RenderConfig(BaseModel):
    preset: str = Field(..., description="Animation preset name")
    duration: float = Field(5.0, ge=3.0, le=15.0, description="Video duration in seconds")
    speed: float = Field(1.0, ge=0.5, le=2.0, description="Animation speed multiplier")
    lighting: str = Field("soft", description="Lighting preset")
    background: BackgroundConfig = BackgroundConfig()
    extrusion: float = Field(0.5, ge=0.1, le=2.0, description="Logo extrusion depth")
    resolution: Literal["1080p", "4K"] = "1080p"
    fps: Literal[24, 30, 60] = 30
    quality: Literal["standard", "high"] = "standard"

class PreviewRequest(BaseModel):
    upload_id: UUID
    config: RenderConfig

class RenderRequest(BaseModel):
    upload_id: UUID
    config: RenderConfig

class JobResponse(BaseModel):
    job_id: UUID
    status: str
    progress: int = 0
    estimated_time: Optional[int] = None
    result_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    error: Optional[str] = None

    class Config:
        from_attributes = True
