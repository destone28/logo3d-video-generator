from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict
import uuid
from pathlib import Path

from ....database import get_db
from ....config import settings
from ....models.upload import Upload
from ....models.render_job import RenderJob, JobType, JobStatus
from ....schemas.render import PreviewRequest, RenderRequest, JobResponse
from ....core.tasks import render_video_task
from ....core.presets import ANIMATION_PRESETS, LIGHTING_PRESETS
from ....services.storage_service import storage_service

router = APIRouter()

@router.get("/presets")
async def get_presets():
    """Get available animation and lighting presets"""
    return {
        "animations": {
            key: {
                "name": preset.name,
                "description": preset.description
            }
            for key, preset in ANIMATION_PRESETS.items()
        },
        "lighting": list(LIGHTING_PRESETS.keys())
    }

@router.post("/preview", response_model=JobResponse)
async def create_preview(
    request: PreviewRequest,
    db: Session = Depends(get_db)
):
    """Create preview render job"""

    # Validate upload exists
    upload = db.query(Upload).filter(Upload.id == request.upload_id).first()
    if not upload:
        raise HTTPException(status_code=404, detail="Upload not found")

    # Validate preset
    if request.config.preset not in ANIMATION_PRESETS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid preset. Available: {', '.join(ANIMATION_PRESETS.keys())}"
        )

    # Validate lighting
    if request.config.lighting not in LIGHTING_PRESETS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid lighting. Available: {', '.join(LIGHTING_PRESETS.keys())}"
        )

    # Create render job
    job = RenderJob(
        id=uuid.uuid4(),
        upload_id=upload.id,
        job_type=JobType.PREVIEW,
        status=JobStatus.QUEUED,
        config=request.config.dict(),
        estimated_duration=int(request.config.duration * 30)  # Rough estimate
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    # Determine which logo to use (processed or original)
    logo_path = upload.processed_path if upload.background_removed else upload.original_path

    # Download logo to local temp
    temp_dir = Path(settings.TEMP_DIR)
    temp_dir.mkdir(parents=True, exist_ok=True)

    local_logo_path = temp_dir / f"{upload.id}.png"

    try:
        object_name = logo_path.split(f"{settings.S3_BUCKET_NAME}/")[-1]
        storage_service.download_file(object_name, str(local_logo_path))
    except Exception as e:
        job.status = JobStatus.FAILED
        job.error_message = f"Failed to download logo: {str(e)}"
        db.commit()
        raise HTTPException(status_code=500, detail=str(e))

    # Queue render task
    render_video_task.delay(
        job_id=str(job.id),
        logo_path=str(local_logo_path),
        config=request.config.dict(),
        is_preview=True
    )

    return JobResponse(
        job_id=job.id,
        status=job.status.value,
        progress=job.progress,
        estimated_time=job.estimated_duration
    )

@router.post("/final", response_model=JobResponse)
async def create_final_render(
    request: RenderRequest,
    db: Session = Depends(get_db)
):
    """Create final render job"""

    # Validate upload exists
    upload = db.query(Upload).filter(Upload.id == request.upload_id).first()
    if not upload:
        raise HTTPException(status_code=404, detail="Upload not found")

    # Validate preset
    if request.config.preset not in ANIMATION_PRESETS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid preset. Available: {', '.join(ANIMATION_PRESETS.keys())}"
        )

    # Validate lighting
    if request.config.lighting not in LIGHTING_PRESETS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid lighting. Available: {', '.join(LIGHTING_PRESETS.keys())}"
        )

    # Create render job
    job = RenderJob(
        id=uuid.uuid4(),
        upload_id=upload.id,
        job_type=JobType.FINAL,
        status=JobStatus.QUEUED,
        config=request.config.dict(),
        estimated_duration=int(request.config.duration * 60)  # Higher quality takes longer
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    # Determine which logo to use (processed or original)
    logo_path = upload.processed_path if upload.background_removed else upload.original_path

    # Download logo to local temp
    temp_dir = Path(settings.TEMP_DIR)
    temp_dir.mkdir(parents=True, exist_ok=True)

    local_logo_path = temp_dir / f"{upload.id}.png"

    try:
        object_name = logo_path.split(f"{settings.S3_BUCKET_NAME}/")[-1]
        storage_service.download_file(object_name, str(local_logo_path))
    except Exception as e:
        job.status = JobStatus.FAILED
        job.error_message = f"Failed to download logo: {str(e)}"
        db.commit()
        raise HTTPException(status_code=500, detail=str(e))

    # Queue render task
    render_video_task.delay(
        job_id=str(job.id),
        logo_path=str(local_logo_path),
        config=request.config.dict(),
        is_preview=False
    )

    return JobResponse(
        job_id=job.id,
        status=job.status.value,
        progress=job.progress,
        estimated_time=job.estimated_duration
    )
