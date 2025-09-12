from __future__ import annotations

from pydantic import BaseModel
from typing import Dict, Any

class ReportRequest(BaseModel):
    candidate_info: Dict[str, Any]
    skill_analysis: Dict[str, Any]
    market_analysis: Dict[str, Any]

class ReportResponse(BaseModel):
    role: str
    markdown_report: str