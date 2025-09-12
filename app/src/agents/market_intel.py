from __future__ import annotations
import json
from langchain_tavily import TavilySearch

from app.src.core.config import settings
from app.src.agents.base import AIBaseAgent
from app.src.schemas.market_intel import MarketIntelResponse

class MarketIntelligenceAgent(AIBaseAgent):
    def analyze(self, role: str) -> MarketIntelResponse:
        search = TavilySearch(max_results=5, tavily_api_key=settings.TAVILY_API_KEY)
        results = search.run(f"{role} job requirements")
        search_results = json.dumps(results, indent=2)
        raw = super().run(
            prompt_template=settings.MARKETING_INTELEGENT_PROMPT,
            variables={
                "role":role,
                "search_results":search_results
            }
        )

        try:
            return MarketIntelResponse(**raw)
        except Exception:
            return raw