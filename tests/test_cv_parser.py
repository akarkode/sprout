import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from fastapi import status
from main import app


@pytest_asyncio.fixture
async def async_client():
    """Provide an AsyncClient instance for all tests using ASGITransport."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_cv_parser_pdf(async_client):
    file_path = "tests/data/john_doe_cv.pdf"
    with open(file_path, "rb") as f:
        response = await async_client.post(
            "/api/agent/cv-parser",
            files={"file": ("john_doe_cv.pdf", f, "application/pdf")},
        )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "John Doe"
    assert any(exp["company"] == "TechCorp Inc." for exp in data["experience"])
    assert "Python" in data["skills"]


@pytest.mark.asyncio
async def test_cv_parser_docx(async_client):
    file_path = "tests/data/john_doe_cv.docx"
    with open(file_path, "rb") as f:
        response = await async_client.post(
            "/api/agent/cv-parser",
            files={"file": ("john_doe_cv.docx", f,
                            "application/vnd.openxmlformats-officedocument.wordprocessingml.document")},
        )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "John Doe"
    assert any("Junior Data Engineer" in exp["position"] for exp in data["experience"])
    assert "Apache Spark" in data["skills"]


@pytest.mark.asyncio
async def test_cv_parser_txt(async_client):
    file_path = "tests/data/john_doe_cv.txt"
    with open(file_path, "rb") as f:
        response = await async_client.post(
            "/api/agent/cv-parser",
            files={"file": ("john_doe_cv.txt", f, "text/plain")},
        )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "John Doe"
    assert any("Data Lakehouse Implementation" in proj["title"] for proj in data["projects"])
    assert "Airflow" in data["skills"]
