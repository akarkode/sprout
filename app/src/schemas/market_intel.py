from __future__ import annotations

from typing import List
from pydantic import BaseModel, Field

class MarketIntelResponse(BaseModel):
    role: str
    in_demand_skills: List[str] = Field(default_factory=list)
    summary: str

class MarketIntelRequest(BaseModel):
    role: str