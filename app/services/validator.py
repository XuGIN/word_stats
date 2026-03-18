from pathlib import Path
from fastapi import HTTPException, UploadFile
from app.core.config import settings

ALLOWRD_EXTENTIONS = [".txt", ".text", ".log", ".md"]

def validate_file_extension(filename: str):
    safe_name = Path(filename).name
    ext = Path(filename).suffix.lower()

    if ext not in ALLOWRD_EXTENTIONS:
        raise HTTPException(status_code=400, detail=f"File extansion {ext} doesn`t support")
    return safe_name
    
def validate_file_size(file: UploadFile):
    size = file.size / (1024*1024)
    if size > settings.MAX_FILE_SIZE_MB:
        raise HTTPException(status_code=400, detail=f"File`s size is too large. Max size is {settings.MAX_FILE_SIZE_MB} mb")
    
def validate_file(file: UploadFile):
    if not file or not file.filename:
        raise HTTPException(status_code=400, detail=f"File not exists")
    
    safe_name = validate_file_extension(file.filename)
    validate_file_size(file)
    return safe_name

