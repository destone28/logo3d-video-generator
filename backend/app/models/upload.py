from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from ..database import Base

class Upload(Base):
    __tablename__ = "uploads"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(String(255), nullable=False)
    original_path = Column(Text, nullable=False)
    thumbnail_path = Column(Text)
    processed_path = Column(Text)
    width = Column(Integer)
    height = Column(Integer)
    file_size = Column(Integer)
    has_transparency = Column(Boolean, default=False)
    background_removed = Column(Boolean, default=False)
    user_session = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
