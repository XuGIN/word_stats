from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from app.core.config import settings
from app.services.analyzer import analyze_file
from app.services.excel_writer import create_excel_report
import os

router = APIRouter()

def cleanup_file(path):
    if path and os.path.exists(path):
        os.remove(path)

@router.post("/public/report/export")
async def process_file(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None
    ):
    file_size_mb = file.size / (1024*1024) if file.size else 0
    if file_size_mb > settings.MAX_FILE_SIZE_MB:
        raise HTTPException(
            status_code=400,
            detail=f"File too large!"
        )
    temp_path = os.path.join(settings.TEMP_PATH, file.filename)
    temp_path_excel = os.path.join(settings.TEMP_PATH, "result.xlsx")
    try:
        with open(temp_path, "wb") as f:
            data = await file.read()
            f.write(data)

        analyzed_file = analyze_file(temp_path)

        create_excel_report(analyzed_file, temp_path_excel)

        background_tasks.add_task(cleanup_file, temp_path)
        background_tasks.add_task(cleanup_file, temp_path_excel)

        return FileResponse(
            path=temp_path_excel,
            filename="result.xlsx",
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        cleanup_file(temp_path)
        raise HTTPException(status_code=500, detail=f"Processing failed: {e}")