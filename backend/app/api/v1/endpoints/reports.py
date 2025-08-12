from fastapi import APIRouter, Depends, HTTPException
from app.services.report_service import ReportService

router = APIRouter()

@router.post("/")
async def generate_report(query: str, report_service: ReportService = Depends()):
    try:
        report_path = await report_service.generate_excel_report(query)
        return {"message": "Report generated successfully", "path": report_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
