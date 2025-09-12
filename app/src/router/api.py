from __future__ import annotations

from fastapi import APIRouter
from fastapi import File, UploadFile

from app.src.agents.report import ReportAgent
from app.src.agents.cv_parser import AICVParser
from app.src.utils.extractor import CVExtractor
from app.src.schemas.cv_parser import CVResponse
from app.src.agents.skill_analyst import SkillAnalystAgent
from app.src.schemas.market_intel import MarketIntelRequest
from app.src.schemas.market_intel import MarketIntelResponse
from app.src.schemas.skill_analyst import SkillAnalysisResponse
from app.src.agents.market_intel import MarketIntelligenceAgent
from app.src.schemas.report import ReportRequest, ReportResponse

router = APIRouter(prefix="/api/agent", tags=["Agent"])

@router.post("/cv-parser", response_model=CVResponse)
async def cv_parser(file:UploadFile=File(...)):
    cv_text = CVExtractor(file_bytes=await file.read(), filename=file.filename).text
    return AICVParser().parse(cv_text=cv_text)

@router.post("/skill-analyst", response_model=SkillAnalysisResponse)
async def skill_analyst(cv_data_json:CVResponse):
    return SkillAnalystAgent().analyze(cv_data_json=cv_data_json)

@router.post("/market-intelligent", response_model=MarketIntelResponse)
async def skill_analyst(body: MarketIntelRequest):
    return MarketIntelligenceAgent().analyze(role=body.role)

@router.post("/report", response_model=ReportResponse)
async def generate_report(body: ReportRequest):
    """
    Node 4: Recommendation & Report Agent
    - Combines candidate info (Node 1), skill analysis (Node 2),
      and market analysis (Node 3) into a final Markdown report.
    """
    agent = ReportAgent()
    report = agent.generate_report(
        candidate_info=body.candidate_info,
        skill_analysis=body.skill_analysis,
        market_analysis=body.market_analysis,
    )
    return report