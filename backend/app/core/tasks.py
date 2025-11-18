from celery import Task
from .celery_app import celery_app
from ..database import SessionLocal
from ..models.render_job import RenderJob, JobStatus
from ..services.blender_renderer import blender_renderer
from ..services.video_encoder import video_encoder
from ..services.storage_service import storage_service
from ..config import settings
from datetime import datetime
import os
import logging
import uuid

logger = logging.getLogger(__name__)

class RenderTask(Task):
    """Base task with database session management"""

    def __call__(self, *args, **kwargs):
        return super().__call__(*args, **kwargs)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """Handle task failure"""
        logger.error(f"Task {task_id} failed: {exc}")
        job_id = kwargs.get("job_id")
        if job_id:
            db = SessionLocal()
            try:
                job = db.query(RenderJob).filter(RenderJob.id == job_id).first()
                if job:
                    job.status = JobStatus.FAILED
                    job.error_message = str(exc)
                    job.completed_at = datetime.utcnow()
                    db.commit()
            finally:
                db.close()

@celery_app.task(base=RenderTask, bind=True)
def render_video_task(self, job_id: str, logo_path: str, config: dict, is_preview: bool = False):
    """Celery task for rendering 3D logo video"""
    db = SessionLocal()

    try:
        # Get job from database
        job = db.query(RenderJob).filter(RenderJob.id == job_id).first()
        if not job:
            raise ValueError(f"Job {job_id} not found")

        # Update job status
        job.status = JobStatus.PROCESSING
        job.started_at = datetime.utcnow()
        job.progress = 0
        db.commit()

        # Generate output filename
        output_filename = f"{job_id}.mp4"
        output_path = os.path.join(settings.RENDER_OUTPUT_DIR, output_filename)

        # Ensure output directory exists
        os.makedirs(settings.RENDER_OUTPUT_DIR, exist_ok=True)

        # Progress callback
        def update_progress(progress: int):
            job.progress = progress
            db.commit()
            self.update_state(state='PROGRESS', meta={'progress': progress})

        # Render video with Blender
        logger.info(f"Starting render for job {job_id}")
        success = blender_renderer.render(
            logo_path=logo_path,
            output_path=output_path,
            config=config,
            is_preview=is_preview,
            progress_callback=update_progress
        )

        if not success:
            raise Exception("Blender rendering failed")

        # Generate thumbnail
        thumbnail_filename = f"{job_id}_thumb.jpg"
        thumbnail_path = os.path.join(settings.RENDER_OUTPUT_DIR, thumbnail_filename)

        video_encoder.create_thumbnail(output_path, thumbnail_path)

        # Upload to storage
        logger.info(f"Uploading render output for job {job_id}")
        video_url = storage_service.upload_file(output_path, f"renders/{output_filename}")
        thumbnail_url = storage_service.upload_file(thumbnail_path, f"renders/{thumbnail_filename}")

        # Update job with results
        job.status = JobStatus.COMPLETED
        job.output_path = video_url
        job.thumbnail_path = thumbnail_url
        job.progress = 100
        job.completed_at = datetime.utcnow()

        # Calculate actual duration
        if job.started_at:
            duration = (job.completed_at - job.started_at).total_seconds()
            job.actual_duration = int(duration)

        db.commit()

        # Clean up local files
        try:
            os.remove(output_path)
            os.remove(thumbnail_path)
        except Exception as e:
            logger.warning(f"Could not clean up files: {e}")

        logger.info(f"Render completed for job {job_id}")

        return {
            "job_id": str(job_id),
            "status": "completed",
            "output_url": video_url,
            "thumbnail_url": thumbnail_url
        }

    except Exception as e:
        logger.error(f"Render task failed: {e}")
        job.status = JobStatus.FAILED
        job.error_message = str(e)
        job.completed_at = datetime.utcnow()
        db.commit()
        raise

    finally:
        db.close()

@celery_app.task
def cleanup_old_renders_task():
    """Periodic task to clean up old render jobs"""
    db = SessionLocal()
    try:
        # Clean up jobs older than 7 days
        from datetime import timedelta
        cutoff_date = datetime.utcnow() - timedelta(days=7)

        old_jobs = db.query(RenderJob).filter(
            RenderJob.created_at < cutoff_date,
            RenderJob.status.in_([JobStatus.COMPLETED, JobStatus.FAILED])
        ).all()

        for job in old_jobs:
            # Delete from storage
            if job.output_path:
                try:
                    # Extract object name from URL
                    object_name = job.output_path.split(f"{settings.S3_BUCKET_NAME}/")[-1]
                    storage_service.delete_file(object_name)
                except Exception as e:
                    logger.warning(f"Could not delete file: {e}")

            if job.thumbnail_path:
                try:
                    object_name = job.thumbnail_path.split(f"{settings.S3_BUCKET_NAME}/")[-1]
                    storage_service.delete_file(object_name)
                except Exception as e:
                    logger.warning(f"Could not delete thumbnail: {e}")

            # Delete job from database
            db.delete(job)

        db.commit()
        logger.info(f"Cleaned up {len(old_jobs)} old render jobs")

    except Exception as e:
        logger.error(f"Cleanup task failed: {e}")
        db.rollback()
    finally:
        db.close()
