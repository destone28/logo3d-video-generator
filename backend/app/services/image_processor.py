from PIL import Image
import cv2
import numpy as np
from rembg import remove
from pathlib import Path
import logging
from typing import Tuple, Optional

logger = logging.getLogger(__name__)

class ImageProcessor:

    @staticmethod
    def get_image_info(image_path: str) -> dict:
        """Extract image metadata"""
        img = Image.open(image_path)
        has_transparency = img.mode in ('RGBA', 'LA') or (
            img.mode == 'P' and 'transparency' in img.info
        )

        return {
            "width": img.width,
            "height": img.height,
            "mode": img.mode,
            "has_transparency": has_transparency,
            "format": img.format
        }

    @staticmethod
    def create_thumbnail(image_path: str, output_path: str, size: Tuple[int, int] = (300, 300)):
        """Create thumbnail of image"""
        img = Image.open(image_path)
        img.thumbnail(size, Image.Resampling.LANCZOS)

        # Convert RGBA to RGB if saving as JPEG
        if img.mode == 'RGBA' and output_path.lower().endswith('.jpg'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])
            img = background

        img.save(output_path, quality=85, optimize=True)
        logger.info(f"Thumbnail created: {output_path}")

    @staticmethod
    def remove_background(input_path: str, output_path: str) -> bool:
        """Remove background from image using rembg"""
        try:
            with open(input_path, 'rb') as input_file:
                input_data = input_file.read()

            output_data = remove(input_data)

            with open(output_path, 'wb') as output_file:
                output_file.write(output_data)

            logger.info(f"Background removed: {output_path}")
            return True
        except Exception as e:
            logger.error(f"Background removal failed: {e}")
            return False

    @staticmethod
    def ensure_rgba(image_path: str, output_path: str):
        """Ensure image is in RGBA format"""
        img = Image.open(image_path)
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        img.save(output_path)

    @staticmethod
    def validate_image(image_path: str) -> bool:
        """Validate if file is a valid image"""
        try:
            img = Image.open(image_path)
            img.verify()
            return True
        except Exception:
            return False

image_processor = ImageProcessor()
