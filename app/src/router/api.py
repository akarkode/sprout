from __future__ import annotations

from fastapi import APIRouter
from fastapi import File, UploadFile

from app.src.agents.cv_parser import AICVParser
from app.src.utils.extractor import CVExtractor
from app.src.schemas.cv_parser import CVResponse

router = APIRouter(prefix="/api/agent", tags=["Agent"])

@router.post("/cv-parser", response_model=CVResponse)
async def cv_parser(file:UploadFile=File(...)):
    cv_text = CVExtractor(file_bytes=await file.read(), filename=file.filename).text
    return CVResponse(**AICVParser().parse(cv_text=cv_text))