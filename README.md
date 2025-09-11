# 🌱 SPROUT  
**Smart Processing for Resume, Opportunities, and Unique Talent**

SPROUT is an AI-powered system designed to streamline the recruitment process by transforming unstructured CVs into structured, machine-readable data.  
The project is built around four main features:  

1. CV Parsing & Normalization (current focus)  
2. Specialized Skill Analysis  
3. Market Intelligence  
4. Recommendation & Report Generation  

This repository currently implements the **CV Parsing & Normalization Agent**.

---

## 🚀 Feature: CV Parsing & Normalization
The **CV Parser Agent** plays the role of a data engineer.  
Its task is to:  

- Input: Ingest a raw CV (PDF, DOCX, or TXT).  
- Process: Extract key information using an AI agent.  
- Output: Structured JSON that can be consumed by downstream systems.  

### Fields Extracted:
- Name  
- Email  
- Phone  
- Education (degree, institution, year)  
- Experience (position, company, years, description)  
- Skills (list)  
- Projects (title, description, technologies)  

---

## ⚙️ Tech Stack
- FastAPI → REST API framework  
- Pydantic → Response schema validation & normalization  
- LangChain + OpenAI → AI agent for text parsing  
- PyPDF2 / python-docx → Text extraction utilities  
- pytest + httpx → Unit testing framework  

---

## 📂 Project Structure (simplified)
```
sprout/
│── app/
│   ├── src/
│   │   ├── agents/
│   │   │   └── cv_parser.py   # AI CV Parser Agent
│   │   ├── utils/
│   │   │   └── extractor.py   # Extractor for PDF/DOCX/TXT
│   │   └── schemas/
│   │       └── cv_parser.py   # Pydantic schema for CV response
│   ├── main.py                # FastAPI entry point
│── tests/
│   ├── data/                  # Test CVs (pdf, docx, txt)
│   └── test_cv_parser.py      # Unit tests for CV parser route
```
---

## ▶️ Running the Application
1. Install dependencies:
   poetry install

2. Set your OpenAI API key:
   export OPENAI_API_KEY=your_api_key_here

3. Start the FastAPI server:
   uvicorn app.main:app --reload

4. Open Swagger UI for testing:
   http://127.0.0.1:8000/docs

Here you can upload a CV file (PDF, DOCX, or TXT) to the `/api/agent/cv-parser` endpoint and see the structured JSON output.

---

## 📝 Example Response
Example response when parsing **John Doe's CV**:

```json
{
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
      "description": "Designed and optimized ETL pipelines using Airflow and Spark. Built data warehouse solutions on AWS Redshift. Collaborated with data scientists to deliver real-time analytics."
    },
    {
      "position": "Junior Data Engineer",
      "company": "DataSolutions LLC",
      "years": "Jul 2018 - Dec 2019",
      "description": "Assisted in developing Python-based ETL pipelines. Managed SQL databases and wrote complex queries. Supported migration of on-premise systems to cloud-based infrastructure."
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
      "technologies": [
        "Kafka",
        "Spark Streaming"
      ]
    },
    {
      "title": "Data Lakehouse Implementation",
      "description": "Led the migration of data warehouse to a lakehouse architecture using Delta Lake.",
      "technologies": [
        "Delta Lake"
      ]
    }
  ]
}
```