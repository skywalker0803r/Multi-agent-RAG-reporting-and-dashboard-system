from fastapi import APIRouter
from app.api.v1.endpoints import reports, dashboards, files

api_router = APIRouter()
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
api_router.include_router(dashboards.router, prefix="/dashboards", tags=["dashboards"])
api_router.include_router(files.router, prefix="/files", tags=["files"])
