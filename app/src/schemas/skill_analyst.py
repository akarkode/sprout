from __future__ import annotations

from pydantic import BaseModel, Field
from typing import List


class SkillAnalysisResponse(BaseModel):
    explicit_skills: List[str] = Field(default_factory=list)
    implicit_skills: List[str] = Field(default_factory=list)
    transferable_skills: List[str] = Field(default_factory=list)
    descriptions: List[str] = Field(default_factory=list)
