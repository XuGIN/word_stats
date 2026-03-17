from fastapi import FastAPI
from app.api.report import router as report_router
from app.services.lemmatizer import get_morph

app = FastAPI()
app.include_router(report_router)

get_morph()

@app.get("/hello")
async def check():
    return {"data": "Hello"}