from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os

router = APIRouter()

REPORTS_DIR = "./reports" # This path is relative to the backend's root

@router.get("/files/{filename}")
async def get_report_file(filename: str):
    file_path = os.path.join(REPORTS_DIR, filename)
    
    # Ensure the file exists and is within the reports directory
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    # Security check: prevent directory traversal
    if not os.path.abspath(file_path).startswith(os.path.abspath(REPORTS_DIR)):
        raise HTTPException(status_code=400, detail="Invalid file path")

    return FileResponse(path=file_path, filename=filename, media_type="application/octet-stream")
