import subprocess
import os
import logging
from typing import Optional
from ..config import settings

logger = logging.getLogger(__name__)

class VideoEncoder:
    """Service for video encoding and post-processing with FFmpeg"""

    @staticmethod
    def create_thumbnail(video_path: str, output_path: str, time_offset: str = "00:00:01") -> bool:
        """Generate thumbnail from video at specified time"""
        try:
            cmd = [
                "ffmpeg",
                "-i", video_path,
                "-ss", time_offset,
                "-vframes", "1",
                "-vf", "scale=320:-1",
                "-y",
                output_path
            ]

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                logger.info(f"Thumbnail created: {output_path}")
                return True
            else:
                logger.error(f"Thumbnail creation failed: {result.stderr}")
                return False

        except Exception as e:
            logger.error(f"Thumbnail creation error: {e}")
            return False

    @staticmethod
    def get_video_info(video_path: str) -> Optional[dict]:
        """Get video metadata using ffprobe"""
        try:
            cmd = [
                "ffprobe",
                "-v", "quiet",
                "-print_format", "json",
                "-show_format",
                "-show_streams",
                video_path
            ]

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                import json
                info = json.loads(result.stdout)
                return info
            else:
                logger.error(f"Video info retrieval failed: {result.stderr}")
                return None

        except Exception as e:
            logger.error(f"Video info error: {e}")
            return None

    @staticmethod
    def optimize_video(input_path: str, output_path: str, quality: str = "standard") -> bool:
        """Optimize video for web delivery"""
        try:
            # Quality settings
            crf = "23" if quality == "standard" else "18"

            cmd = [
                "ffmpeg",
                "-i", input_path,
                "-c:v", "libx264",
                "-preset", "medium",
                "-crf", crf,
                "-c:a", "aac",
                "-b:a", "128k",
                "-movflags", "+faststart",
                "-y",
                output_path
            ]

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                logger.info(f"Video optimized: {output_path}")
                return True
            else:
                logger.error(f"Video optimization failed: {result.stderr}")
                return False

        except Exception as e:
            logger.error(f"Video optimization error: {e}")
            return False

video_encoder = VideoEncoder()
