from __future__ import annotations

from fastapi import APIRouter
from fastapi import File, UploadFile

from app.src.agents.cv_parser import AICVParser
from app.src.utils.extractor import CVExtractor
from app.src.schemas.cv_parser import CVResponse
from app.src.agents.skill_analyst import SkillAnalystAgent
from app.src.schemas.skill_analyst import SkillAnalysisResponse

router = APIRouter(prefix="/api/agent", tags=["Agent"])

@router.post("/cv-parser", response_model=CVResponse)
async def cv_parser(file:UploadFile=File(...)):
    cv_text = CVExtractor(file_bytes=await file.read(), filename=file.filename).text
    return AICVParser().parse(cv_text=cv_text)

@router.post("/skill-analyst", response_model=SkillAnalysisResponse)
async def skill_analyst(cv_data_json:CVResponse):
    return SkillAnalystAgent().analyze(cv_data_json=cv_data_json)