import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from fastapi import status

from main import app
from app.src.agents.market_intel import MarketIntelligenceAgent


@pytest_asyncio.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


def test_market_intel_agent(monkeypatch):
    """Unit test for MarketIntelligenceAgent with monkeypatched Tavily results"""

    fake_results = [
        {
            "title": "Senior AI Engineer Job - LinkedIn",
            "url": "https://www.linkedin.com/jobs/view/12345",
            "content": "Requirements: Python, PyTorch, TensorFlow, AWS, MLOps"
        },
        {
            "title": "Senior AI Engineer Description - Indeed",
            "url": "https://www.indeed.com/viewjob/6789",
            "content": "Key skills: Machine Learning, Kubernetes, Cloud, CI/CD pipelines"
        }
    ]

    # Monkeypatch Tavily search
    def fake_search_run(self, query: str):
        return fake_results

    monkeypatch.setattr("app.src.agents.market_intel.TavilySearch.run", fake_search_run)

    agent = MarketIntelligenceAgent()
    result = agent.analyze("Senior AI Engineer")

    assert "role" in result.model_dump()
    assert "in_demand_skills" in result.model_dump()
    assert "summary" in result.model_dump()
    assert "Python" in result.in_demand_skills


@pytest.mark.asyncio
async def test_market_intel_endpoint(async_client, monkeypatch):
    """Integration test for /api/agent/market-intel endpoint"""

    fake_results = [
        {
            "title": "AI Engineer Job - Example",
            "url": "https://example.com/jobs/ai",
            "content": "Requirements: Python, TensorFlow, MLOps, Cloud"
        }
    ]

    def fake_search_run(self, query: str):
        return fake_results

    monkeypatch.setattr("app.src.agents.market_intel.TavilySearch.run", fake_search_run)

    response = await async_client.post("/api/agent/market-intelligent", json={"role": "AI Engineer"})
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data["role"] == "AI Engineer"
    assert "Python" in data["in_demand_skills"]
    assert isinstance(data["summary"], str)
