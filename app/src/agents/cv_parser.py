from __future__ import annotations

from app.src.core.config import settings
from app.src.agents.base import AIBaseAgent
from app.src.schemas.cv_parser import CVResponse


class AICVParser(AIBaseAgent):
    "AICVParser: Agent for parsing CVs using OpenAI API via LangChain."
    def parse(self, cv_text: str) -> CVResponse:
        raw = super().run(prompt_template=settings.CV_PARSER_PROMPT, variables={"cv_text":cv_text})
        try:
            return CVResponse(**raw)
        except Exception:
            return raw