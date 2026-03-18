from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from app.core.config import settings
from app.services.analyzer import analyze_file
from app.services.excel_writer import create_excel_report
from app.services.validator import validate_file
import aiofiles
import os
import uuid

router = APIRouter()

def cleanup_file(path):
    if path and os.path.exists(path):
        os.remove(path)

@router.post("/public/report/export")
async def process_file(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None
    ):
    safe_name = validate_file(file)
    unique_id = uuid.uuid4().hex
    temp_filename = f"{unique_id}_{safe_name}"
    temp_path = os.path.join(settings.TEMP_PATH, temp_filename)
    temp_path_excel = os.path.join(settings.TEMP_PATH, f"result_{unique_id}.xlsx")
    try:
        async with aiofiles.open(temp_path, "wb") as f:
            while True:
                data = await file.read(1024*1024)
                if not data:
                    break
                await f.write(data)

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