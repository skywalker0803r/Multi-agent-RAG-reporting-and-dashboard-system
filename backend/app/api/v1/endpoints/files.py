from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os
from pathlib import Path

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent # Go up to the project root
REPORTS_DIR = BASE_DIR / "backend" / "reports"

@router.get("/files/{filename}")
async def get_report_file(filename: str):
    file_path = REPORTS_DIR / filename # Use Path object for joining
    
    # Ensure the file exists and is within the reports directory
    print(f"DEBUG: Attempting to serve file from resolved path: {file_path.resolve()}") # New debug print
    print(f"DEBUG: file_path.exists(): {file_path.exists()}") # New debug print
    print(f"DEBUG: file_path.is_file(): {file_path.is_file()}") # New debug print

    if not file_path.exists() or not file_path.is_file(): # Use Path methods
        print(f"DEBUG: Inside 404 block - file not found or not a file.") # New debug print
        raise HTTPException(status_code=404, detail="File not found")
    
    # Security check: prevent directory traversal
    if not str(file_path.resolve()).startswith(str(REPORTS_DIR.resolve())):
        print(f"DEBUG: Inside 400 block - security check failed.") # New debug print
        raise HTTPException(status_code=400, detail="Invalid file path")

    return FileResponse(path=str(file_path), filename=filename, media_type="application/octet-stream")
