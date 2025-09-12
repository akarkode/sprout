from __future__ import annotations

from fastapi import APIRouter, UploadFile, File
from app.src.utils.extractor import CVExtractor
from app.src.orchestration.pipeline import pipeline
from app.src.schemas.report import ReportResponse

router = APIRouter(prefix="/orchestration", tags=["Pipeline"])

@router.post("/pipeline", response_model=ReportResponse)
async def run_pipeline(file: UploadFile = File(...), role: str = "Senior AI Engineer"):
    """
    Full Pipeline Orchestration
    Node 1 → Node 2 → Node 3 → Node 4
    Input: CV file + target role
    Output: Final Markdown report
    """
    cv_text = CVExtractor(file_bytes=await file.read(), filename=file.filename)._extract_text()
    final_state = pipeline.invoke({"cv_text": cv_text, "role": role})
    return final_state["report"]
