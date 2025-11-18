from fastapi import Depends
from sqlalchemy.orm import Session
from .database import get_db
from .config import get_settings, Settings

def get_settings_dependency() -> Settings:
    return get_settings()
