from fastapi import APIRouter, Depends, HTTPException
from app.services.dashboard_service import DashboardService

router = APIRouter()

@router.get("/")
async def get_dashboard_data(query: str, dashboard_service: DashboardService = Depends()):
    try:
        data = await dashboard_service.get_dashboard_data(query)
        return {"message": "Dashboard data retrieved successfully", "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
