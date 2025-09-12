import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from fastapi import status

from main import app
from app.src.orchestration.pipeline import pipeline
from app.src.schemas.market_intel import MarketIntelResponse
from app.src.schemas.report import ReportResponse
from app.src.schemas.cv_parser import CVResponse
from app.src.schemas.skill_analyst import SkillAnalysisResponse


@pytest_asyncio.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


def test_pipeline_direct(monkeypatch):
    """Unit test pipeline orchestration directly with monkeypatched agents"""

    fake_cv_text = "John Doe, Backend Engineer skilled in Python and AWS."

    # Monkeypatch CV Parser
    monkeypatch.setattr(
        "app.src.agents.cv_parser.AICVParser.parse",
        lambda self, cv_text: CVResponse(**{"name": "John Doe", "skills": ["Python", "AWS"]})
    )

    # Monkeypatch Skill Analyst
    monkeypatch.setattr(
        "app.src.agents.skill_analyst.SkillAnalystAgent.analyze",
        lambda self, parsed_cv: SkillAnalysisResponse(**{
            "explicit_skills": ["Python", "AWS"],
            "implicit_skills": ["ETL"],
            "transferable_skills": ["Problem Solving"],
            "description": ["Python and AWS explicit, ETL inferred."]
        })
    )

    # Monkeypatch Market Intelligence
    monkeypatch.setattr(
        "app.src.agents.market_intel.MarketIntelligenceAgent.analyze",
        lambda self, role: MarketIntelResponse(
            role=role,
            in_demand_skills=["Python", "TensorFlow", "MLOps"],
            summary="Market expects Python, TensorFlow, and MLOps."
        )
    )

    # Monkeypatch Report Agent
    monkeypatch.setattr(
        "app.src.agents.report.ReportAgent.generate_report",
        lambda self, **kwargs: ReportResponse(
            role=kwargs["market_analysis"].get("role"),
            markdown_report=f"# Report for {kwargs['candidate_info']['name']} ({kwargs['market_analysis'].get("role")})"
        )
    )

    result = pipeline.invoke({"cv_text": fake_cv_text, "role": "Senior AI Engineer"})

    assert "report" in result
    assert "markdown_report" in result["report"]
    assert "Senior AI Engineer" in result["report"]["markdown_report"]


@pytest.mark.asyncio
async def test_pipeline_endpoint(async_client, monkeypatch):
    """Integration test /api/orchestration/pipeline endpoint"""

    # Monkeypatch agents
    monkeypatch.setattr(
        "app.src.agents.cv_parser.AICVParser.parse",
        lambda self, cv: CVResponse(**{"name": "Jane Doe", "skills": ["Python"]})
    )
    monkeypatch.setattr(
        "app.src.agents.skill_analyst.SkillAnalystAgent.analyze",
        lambda self, parsed: SkillAnalysisResponse(**{"explicit_skills": ["Python"], "implicit_skills": [], "transferable_skills": [], "description": []})
    )
    monkeypatch.setattr(
        "app.src.agents.market_intel.MarketIntelligenceAgent.analyze",
        lambda self, role: MarketIntelResponse(
            role=role,
            in_demand_skills=["Python"],
            summary="Python is in demand."
        )
    )
    monkeypatch.setattr(
        "app.src.agents.report.ReportAgent.generate_report",
        lambda self, **kwargs: ReportResponse(
            role=kwargs["market_analysis"].get("role"),
            markdown_report="# Fake Report"
        )
    )

    # Simulate CV upload
    file_content = b"Jane Doe CV content"
    files = {"file": ("jane_doe.txt", file_content, "text/plain")}

    response = await async_client.post("/api/orchestration/pipeline?role=Data Engineer", files=files)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["role"] == "Data Engineer"
    assert "markdown_report" in data
    assert "# Fake Report" in data["markdown_report"]
