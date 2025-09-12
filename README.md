# 🌱 SPROUT  
**Smart Processing for Resume, Opportunities, and Unique Talent**

SPROUT is an AI-powered system designed to streamline the recruitment process by transforming unstructured CVs into structured, machine-readable data.  
The project is built around four main features:  

1. CV Parsing & Normalization  
2. Specialized Skill Analysis (newly added)  
3. Market Intelligence  
4. Recommendation & Report Generation  

This repository currently implements:  
- The **CV Parsing & Normalization Agent** (Point 1)  
- The **Specialized Skill Analyst Agent** (Point 2)  

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

## 🚀 Feature: Specialized Skill Analyst
The **Skill Analyst Agent** plays the role of a subject matter expert.  
Its task is to:  

- Input: Structured JSON data from the CV Parser Agent.  
- Process: Analyze explicit skills, infer implicit skills from projects/experience, and identify transferable skills.  
- Output: Enhanced structured JSON with skill categorization.  

### Fields Extracted:
- explicit_skills → directly listed in the CV  
- implicit_skills → inferred from experience and projects  
- transferable_skills → applicable across multiple domains  
- description → reasoning for implicit and transferable skills  

---

## ⚙️ Tech Stack
- FastAPI → REST API framework  
- Pydantic → Response schema validation & normalization  
- LangChain + OpenAI → AI agent for text parsing and skill analysis  
- PyPDF2 / python-docx → Text extraction utilities  
- pytest + httpx → Unit testing framework  

---

## 📂 Project Structure (simplified)
```
sprout/
│── app/
│   ├── src/
│   │   ├── agents/
│   │   │   ├── base.py             # AI Base Agent
│   │   │   ├── cv_parser.py        # AI CV Parser Agent
│   │   │   └── skill_analyst.py    # AI Skill Analyst Agent
│   │   ├── utils/
│   │   │   └── extractor.py        # Extractor for PDF/DOCX/TXT
│   │   └── schemas/
│   │       ├── cv_parser.py        # Pydantic schema for CV response
│   │       └── skill_analysis.py   # Pydantic schema for Skill Analyst response
│   ├── main.py                     # FastAPI entry point
│── tests/
│   ├── data/                       # Test CVs (pdf, docx, txt)
│   ├── test_cv_parser.py           # Unit tests for CV parser route
│   └── test_skill_analyst.py       # Unit tests for skill analyst route
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

Endpoints available:
- POST `/api/agent/cv-parser` → upload CV file and get structured JSON  
- POST `/api/agent/skill-analyst` → analyze structured JSON for skills  

---

## 📝 Example Response (CV Parser)
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
---

## 📝 Example Response (Skill Analyst)
Example response when analyzing **John Doe's CV structured JSON**:
```json
{
  "explicit_skills": [
    "Python",
    "SQL",
    "Apache Spark",
    "Airflow",
    "AWS",
    "Docker",
    "Kubernetes",
    "Data Warehousing"
  ],
  "implicit_skills": [
    "ETL Design",
    "Cloud Architecture",
    "Real-time Data Processing",
    "Data Migration"
  ],
  "transferable_skills": [
    "Problem Solving",
    "Collaboration",
    "System Design"
  ],
  "description": [
    "ETL Design inferred from Airflow pipelines.",
    "Cloud Architecture inferred from AWS migration.",
    "System Design transferable from building large-scale pipelines."
  ]
}
```