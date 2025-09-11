from __future__ import annotations

from pydantic import BaseModel, Field
from typing import List, Optional


class Education(BaseModel):
    degree: str
    institution: str
    year: Optional[str] = None


class Experience(BaseModel):
    position: str
    company: str
    years: Optional[str] = None
    description: Optional[str] = None


class Project(BaseModel):
    title: str
    description: Optional[str] = None
    technologies: Optional[List[str]] = None


class CVResponse(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    education: List[Education] = Field(default_factory=list)
    experience: List[Experience] = Field(default_factory=list)
    skills: List[str] = Field(default_factory=list)
    projects: List[Project] = Field(default_factory=list)
