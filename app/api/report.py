from fastapi import APIRouter, UploadFile, File, HTTPException
from app.core.config import settings
import os

router = APIRouter()

@router.post("/public/report/export")
async def get_file(file: UploadFile = File(...)):
    file_size_mb = file.size / (1024*1024) if file.size else 0
    if file_size_mb > settings.MAX_FILE_SIZE_MB:
        raise HTTPException(
            status_code=400,
            detail=f"File too large!"
        )
    temp_path = os.path.join(settings.TEMP_PATH, file.filename)
    try:
        with open(temp_path, "wb") as f:
            data = await file.read()
            f.write(data)

        return {
            "message": "File uploaded successfilly",
            "filename": file.filename,
            "size_mb": file_size_mb,
        }
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)