from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
import os
import uuid
from pathlib import Path
import aiofiles

from ....database import get_db
from ....config import settings
from ....models.upload import Upload
from ....schemas.upload import UploadResponse, BackgroundRemovalRequest, BackgroundRemovalResponse
from ....services.image_processor import image_processor
from ....services.storage_service import storage_service

router = APIRouter()

@router.post("/", response_model=UploadResponse)
async def upload_logo(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload logo image"""

    # Validate file extension
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Allowed types: {', '.join(settings.ALLOWED_EXTENSIONS)}"
        )

    # Validate file size
    contents = await file.read()
    file_size = len(contents)

    if file_size > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Max size: {settings.MAX_UPLOAD_SIZE / (1024 * 1024)}MB"
        )

    # Generate unique filename
    upload_id = uuid.uuid4()
    filename = f"{upload_id}{file_ext}"

    # Save to temporary location
    temp_dir = Path(settings.TEMP_DIR)
    temp_dir.mkdir(parents=True, exist_ok=True)

    temp_path = temp_dir / filename

    async with aiofiles.open(temp_path, 'wb') as f:
        await f.write(contents)

    # Validate image
    if not image_processor.validate_image(str(temp_path)):
        os.remove(temp_path)
        raise HTTPException(status_code=400, detail="Invalid image file")

    # Get image info
    image_info = image_processor.get_image_info(str(temp_path))

    # Create thumbnail
    thumbnail_filename = f"{upload_id}_thumb.jpg"
    thumbnail_path = temp_dir / thumbnail_filename
    image_processor.create_thumbnail(str(temp_path), str(thumbnail_path))

    # Upload to storage
    try:
        original_url = storage_service.upload_file(
            str(temp_path),
            f"uploads/{filename}"
        )
        thumbnail_url = storage_service.upload_file(
            str(thumbnail_path),
            f"uploads/{thumbnail_filename}"
        )
    except Exception as e:
        # Clean up temp files
        if temp_path.exists():
            os.remove(temp_path)
        if thumbnail_path.exists():
            os.remove(thumbnail_path)
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

    # Create database record
    upload_record = Upload(
        id=upload_id,
        filename=file.filename,
        original_path=original_url,
        thumbnail_path=thumbnail_url,
        width=image_info["width"],
        height=image_info["height"],
        file_size=file_size,
        has_transparency=image_info["has_transparency"],
        background_removed=False
    )

    db.add(upload_record)
    db.commit()
    db.refresh(upload_record)

    # Clean up temp files
    if temp_path.exists():
        os.remove(temp_path)
    if thumbnail_path.exists():
        os.remove(thumbnail_path)

    return UploadResponse(
        upload_id=upload_record.id,
        filename=upload_record.filename,
        thumbnail_url=upload_record.thumbnail_path,
        original_url=upload_record.original_path,
        width=upload_record.width,
        height=upload_record.height,
        file_size=upload_record.file_size,
        has_transparency=upload_record.has_transparency,
        background_removed=upload_record.background_removed,
        created_at=upload_record.created_at
    )

@router.post("/remove-background", response_model=BackgroundRemovalResponse)
async def remove_background(
    request: BackgroundRemovalRequest,
    db: Session = Depends(get_db)
):
    """Remove background from uploaded image"""

    # Get upload record
    upload = db.query(Upload).filter(Upload.id == request.upload_id).first()
    if not upload:
        raise HTTPException(status_code=404, detail="Upload not found")

    # Download original image
    temp_dir = Path(settings.TEMP_DIR)
    temp_dir.mkdir(parents=True, exist_ok=True)

    input_filename = f"{upload.id}_original.png"
    output_filename = f"{upload.id}_nobg.png"

    input_path = temp_dir / input_filename
    output_path = temp_dir / output_filename

    try:
        # Download from storage
        object_name = upload.original_path.split(f"{settings.S3_BUCKET_NAME}/")[-1]
        storage_service.download_file(object_name, str(input_path))

        # Remove background
        success = image_processor.remove_background(str(input_path), str(output_path))

        if not success:
            raise Exception("Background removal failed")

        # Upload processed image
        processed_url = storage_service.upload_file(
            str(output_path),
            f"uploads/{output_filename}"
        )

        # Update upload record
        upload.processed_path = processed_url
        upload.background_removed = True
        db.commit()

        # Clean up temp files
        if input_path.exists():
            os.remove(input_path)
        if output_path.exists():
            os.remove(output_path)

        return BackgroundRemovalResponse(
            upload_id=upload.id,
            processed_url=processed_url,
            success=True
        )

    except Exception as e:
        # Clean up temp files
        if input_path.exists():
            os.remove(input_path)
        if output_path.exists():
            os.remove(output_path)

        raise HTTPException(status_code=500, detail=f"Background removal failed: {str(e)}")

@router.get("/{upload_id}", response_model=UploadResponse)
async def get_upload(upload_id: uuid.UUID, db: Session = Depends(get_db)):
    """Get upload details"""
    upload = db.query(Upload).filter(Upload.id == upload_id).first()
    if not upload:
        raise HTTPException(status_code=404, detail="Upload not found")

    return UploadResponse(
        upload_id=upload.id,
        filename=upload.filename,
        thumbnail_url=upload.thumbnail_path,
        original_url=upload.original_path,
        width=upload.width,
        height=upload.height,
        file_size=upload.file_size,
        has_transparency=upload.has_transparency,
        background_removed=upload.background_removed,
        created_at=upload.created_at
    )
