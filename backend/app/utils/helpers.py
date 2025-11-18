import hashlib
import os
from typing import Optional
from datetime import datetime, timedelta

def generate_file_hash(file_path: str) -> str:
    """Generate SHA256 hash of file"""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"

def format_duration(seconds: int) -> str:
    """Format duration in human-readable format"""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes}m {secs}s"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours}h {minutes}m"

def estimate_render_time(
    resolution: str,
    duration: float,
    quality: str,
    fps: int = 30
) -> int:
    """Estimate render time in seconds"""
    # Base time per frame (rough estimates)
    base_time_per_frame = {
        "1080p": {
            "standard": 2,  # 2 seconds per frame
            "high": 4
        },
        "4K": {
            "standard": 8,
            "high": 15
        }
    }

    time_per_frame = base_time_per_frame.get(resolution, {}).get(quality, 2)
    total_frames = duration * fps
    estimated_time = int(total_frames * time_per_frame)

    return estimated_time

def clean_temp_files(directory: str, max_age_hours: int = 24):
    """Clean temporary files older than specified hours"""
    if not os.path.exists(directory):
        return

    cutoff_time = datetime.now() - timedelta(hours=max_age_hours)

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            if file_time < cutoff_time:
                try:
                    os.remove(file_path)
                except Exception:
                    pass  # Ignore errors

def parse_blender_version(version_string: str) -> Optional[tuple]:
    """Parse Blender version string"""
    try:
        import re
        match = re.search(r'(\d+)\.(\d+)\.(\d+)', version_string)
        if match:
            return tuple(map(int, match.groups()))
    except Exception:
        pass
    return None
