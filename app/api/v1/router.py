from fastapi import APIRouter

from app.api.v1.endpoints import analyze, upload, health

api_router = APIRouter()

# Core routes
api_router.include_router(
    analyze.router,
    prefix="/analyze",
    tags=["Analyze"]
)

api_router.include_router(
    upload.router,
    prefix="/upload",
    tags=["Upload"]
)

api_router.include_router(
    health.router,
    prefix="/health",
    tags=["Health"]
)