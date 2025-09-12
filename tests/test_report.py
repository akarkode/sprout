import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from fastapi import status

from main import app
from app.src.agents.report import ReportAgent


@pytest_asyncio.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


def test_report_agent_generate():
    """Unit test ReportAgent.generate_report with fake inputs"""

    candidate_info = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "skills": ["Python", "SQL", "Airflow"]
    }
    skill_analysis = {
        "explicit_skills": ["Python", "SQL"],
        "implicit_skills": ["ETL Design"],
        "transferable_skills": ["Problem Solving"],
        "description": ["Python and SQL from explicit, ETL inferred, problem solving transferable."]
    }
    market_analysis = {
        "role": "Senior AI Engineer",
        "in_demand_skills": ["Python", "PyTorch", "TensorFlow", "MLOps"],
        "summary": "Market expects Python, deep learning frameworks, and MLOps."
    }

    agent = ReportAgent()
    result = agent.generate_report(candidate_info, skill_analysis, market_analysis)

    assert isinstance(result.markdown_report, str)
    assert "John Doe" in result.markdown_report
    assert "Senior AI Engineer" in result.markdown_report
    assert "MLOps" in result.markdown_report


@pytest.mark.asyncio
async def test_report_endpoint(async_client):
    """Integration test /api/agent/report endpoint"""

    body = {
        "candidate_info": {"name": "Jane Doe", "email": "jane@example.com", "skills": ["Python", "SQL"]},
        "skill_analysis": {
            "explicit_skills": ["Python"],
            "implicit_skills": ["ETL Design"],
            "transferable_skills": ["Team Collaboration"],
            "description": ["ETL inferred, collaboration transferable."]
        },
        "market_analysis": {
            "role": "Data Engineer",
            "in_demand_skills": ["Python", "Spark", "AWS"],
            "summary": "Data Engineers need strong Python, Spark, and AWS skills."
        }
    }

    response = await async_client.post("/api/agent/report", json=body)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["role"] == "Data Engineer"
    assert "markdown_report" in data
    assert "Data Engineer" in data["markdown_report"]
