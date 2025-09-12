from __future__ import annotations

from app.src.core.config import settings
from app.src.agents.base import AIBaseAgent
from app.src.schemas.cv_parser import CVResponse
from app.src.schemas.skill_analyst import SkillAnalysisResponse


class SkillAnalystAgent(AIBaseAgent):
    "SkillAnalystAgent: Agent for Anlysist Skill CVs (JSON) using OpenAI API via LangChain."
    def analyze(self, cv_data_json: CVResponse) -> SkillAnalysisResponse:
        raw = super().run(
            prompt_template=settings.SKILL_ANALYST_PROMPT,
            variables={"cv_data_json":cv_data_json}
        )
        try:
            return SkillAnalysisResponse(**raw)
        except Exception:
            return raw
