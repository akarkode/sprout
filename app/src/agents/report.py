from __future__ import annotations

import json
from app.src.core.config import settings
from app.src.agents.base import AIBaseAgent
from app.src.schemas.report import ReportResponse


class ReportAgent(AIBaseAgent):
    def generate_report(self, candidate_info: dict, skill_analysis: dict, market_analysis: dict) -> ReportResponse:
        raw = super().run(
            prompt_template=settings.REPORT_PROMPT,
            variables={
                "candidate_info": json.dumps(candidate_info, indent=2),
                "skill_analysis": json.dumps(skill_analysis, indent=2),
                "market_analysis": json.dumps(market_analysis, indent=2),
            }
        )

        try:
            return ReportResponse(role=market_analysis.get("role", "Unknown Role"), markdown_report=raw if isinstance(raw, str) else raw.get("raw_output", ""))
        except Exception:
            return ReportResponse(role="Unknown Role", markdown_report=str(raw))