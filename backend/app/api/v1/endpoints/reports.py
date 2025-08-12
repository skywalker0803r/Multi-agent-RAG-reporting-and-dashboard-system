from fastapi import APIRouter, Depends, HTTPException, Body
from app.services.report_service import ReportService

router = APIRouter()

@router.post("/")
async def generate_report(query: str = Body(..., embed=True), report_service: ReportService = Depends()):
    try:
        report_path, report_content = await report_service.generate_excel_report(query)
        return {"message": "報告生成成功", "path": report_path, "content": report_content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
