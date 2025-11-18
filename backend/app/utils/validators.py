import re
from typing import Optional
from pathlib import Path

def validate_hex_color(color: str) -> bool:
    """Validate hex color format"""
    pattern = r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'
    return bool(re.match(pattern, color))

def validate_file_extension(filename: str, allowed_extensions: set) -> bool:
    """Validate file extension"""
    ext = Path(filename).suffix.lower()
    return ext in allowed_extensions

def validate_image_dimensions(width: int, height: int, max_size: int = 4096) -> bool:
    """Validate image dimensions"""
    return 0 < width <= max_size and 0 < height <= max_size

def validate_aspect_ratio(width: int, height: int, max_ratio: float = 10.0) -> bool:
    """Validate aspect ratio is reasonable"""
    if height == 0:
        return False
    ratio = width / height
    return 1/max_ratio <= ratio <= max_ratio

def sanitize_filename(filename: str) -> str:
    """Sanitize filename to prevent path traversal"""
    # Remove path separators and dangerous characters
    filename = re.sub(r'[/\\]', '', filename)
    filename = re.sub(r'[^\w\s.-]', '', filename)
    return filename[:255]  # Limit length
