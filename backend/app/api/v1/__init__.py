from fastapi import APIRouter
from .endpoints import upload, render, jobs, health

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(upload.router, prefix="/upload", tags=["upload"])
api_router.include_router(render.router, prefix="/render", tags=["render"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
