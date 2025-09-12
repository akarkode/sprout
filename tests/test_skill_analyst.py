import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from fastapi import status
from main import app


@pytest_asyncio.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_skill_analyst_endpoint(async_client):
    # Structured CV data (from parser output)
    body = {
      "name": "John Doe",
      "email": "john.doe@example.com",
      "phone": "+1 234 567 890",
      "education": [
        {
          "degree": "B.Sc. in Computer Science",
          "institution": "University of California, Berkeley",
          "year": "2014 - 2018"
        }
      ],
      "experience": [
        {
          "position": "Data Engineer",
          "company": "TechCorp Inc.",
          "years": "Jan 2020 - Present",
          "description": "- Designed and optimized ETL pipelines using Airflow and Spark.\n- Built data warehouse solutions on AWS Redshift.\n- Collaborated with data scientists to deliver real-time analytics."
        },
        {
          "position": "Junior Data Engineer",
          "company": "DataSolutions LLC",
          "years": "Jul 2018 - Dec 2019",
          "description": "- Assisted in developing Python-based ETL pipelines.\n- Managed SQL databases and wrote complex queries.\n- Supported migration of on-premise systems to cloud-based infrastructure."
        }
      ],
      "skills": [
        "Python",
        "SQL",
        "Apache Spark",
        "Airflow",
        "AWS",
        "Docker",
        "Kubernetes",
        "Data Warehousing"
      ],
      "projects": [
        {
          "title": "Real-Time Analytics Platform",
          "description": "Developed a real-time data ingestion system using Kafka and Spark Streaming.",
          "technologies": ["Kafka", "Spark Streaming"]
        },
        {
          "title": "Data Lakehouse Implementation",
          "description": "Led the migration of data warehouse to a lakehouse architecture using Delta Lake.",
          "technologies": ["Delta Lake"]
        }
      ]
    }

    response = await async_client.post("/api/agent/skill-analyst", json=body)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    # check schema fields exist
    assert "explicit_skills" in data
    assert "implicit_skills" in data
    assert "transferable_skills" in data
    assert "descriptions" in data

    # sanity check: explicit should include known skills
    for skill in ["Python", "SQL", "Airflow"]:
        assert skill in data["explicit_skills"]
