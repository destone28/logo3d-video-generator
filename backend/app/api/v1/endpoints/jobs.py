from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid

from ....database import get_db
from ....models.render_job import RenderJob, JobStatus
from ....schemas.job import JobStatusResponse, RenderHistoryItem

router = APIRouter()

@router.get("/{job_id}", response_model=JobStatusResponse)
async def get_job_status(job_id: uuid.UUID, db: Session = Depends(get_db)):
    """Get status of a render job"""
    job = db.query(RenderJob).filter(RenderJob.id == job_id).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Calculate estimated remaining time
    estimated_remaining = None
    if job.status == JobStatus.PROCESSING and job.estimated_duration:
        if job.progress > 0:
            elapsed_ratio = job.progress / 100
            if elapsed_ratio < 1:
                estimated_total = job.estimated_duration / elapsed_ratio
                if job.started_at:
                    from datetime import datetime
                    elapsed = (datetime.utcnow() - job.started_at).total_seconds()
                    estimated_remaining = int(estimated_total - elapsed)

    return JobStatusResponse(
        job_id=job.id,
        status=job.status.value,
        progress=job.progress,
        estimated_remaining=estimated_remaining,
        result_url=job.output_path,
        thumbnail_url=job.thumbnail_path,
        error_message=job.error_message,
        created_at=job.created_at,
        started_at=job.started_at,
        completed_at=job.completed_at
    )

@router.delete("/{job_id}")
async def cancel_job(job_id: uuid.UUID, db: Session = Depends(get_db)):
    """Cancel a queued or processing job"""
    job = db.query(RenderJob).filter(RenderJob.id == job_id).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    if job.status in [JobStatus.COMPLETED, JobStatus.FAILED]:
        raise HTTPException(status_code=400, detail="Job already finished")

    # For now, just mark as failed
    # In production, you would also revoke the Celery task
    job.status = JobStatus.FAILED
    job.error_message = "Cancelled by user"
    from datetime import datetime
    job.completed_at = datetime.utcnow()

    db.commit()

    return {"message": "Job cancelled successfully"}

@router.get("/upload/{upload_id}/history", response_model=List[RenderHistoryItem])
async def get_render_history(
    upload_id: uuid.UUID,
    db: Session = Depends(get_db),
    limit: int = 10
):
    """Get render history for an upload"""
    jobs = db.query(RenderJob).filter(
        RenderJob.upload_id == upload_id
    ).order_by(
        RenderJob.created_at.desc()
    ).limit(limit).all()

    history = []
    for job in jobs:
        config = job.config or {}
        history.append(RenderHistoryItem(
            render_id=job.id,
            created_at=job.created_at,
            status=job.status.value,
            config=config,
            thumbnail_url=job.thumbnail_path,
            video_url=job.output_path,
            duration=config.get("duration", 0),
            resolution=config.get("resolution", "1080p"),
            file_size=None  # Could be calculated if needed
        ))

    return history

@router.get("/", response_model=List[JobStatusResponse])
async def list_jobs(
    db: Session = Depends(get_db),
    status: str = None,
    limit: int = 20
):
    """List recent render jobs"""
    query = db.query(RenderJob)

    if status:
        try:
            status_enum = JobStatus(status)
            query = query.filter(RenderJob.status == status_enum)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid status: {status}")

    jobs = query.order_by(RenderJob.created_at.desc()).limit(limit).all()

    return [
        JobStatusResponse(
            job_id=job.id,
            status=job.status.value,
            progress=job.progress,
            estimated_remaining=None,
            result_url=job.output_path,
            thumbnail_url=job.thumbnail_path,
            error_message=job.error_message,
            created_at=job.created_at,
            started_at=job.started_at,
            completed_at=job.completed_at
        )
        for job in jobs
    ]
