# 🌱 SPROUT  
**Smart Processing for Resume, Opportunities, and Unique Talent**

SPROUT is an AI-powered system designed to streamline the recruitment process by transforming unstructured CVs into structured, machine-readable data.  
The project is built around four main features:  

1. CV Parsing & Normalization  
2. Specialized Skill Analysis  
3. Market Intelligence (newly added)  
4. Recommendation & Report Generation (to be implemented)  

This repository currently implements:  
- **CV Parsing & Normalization Agent** (Point 1)  
- **Specialized Skill Analyst Agent** (Point 2)  
- **Market Intelligence Agent** (Point 3)  

---

## 🚀 Feature: CV Parsing & Normalization
The **CV Parser Agent** plays the role of a data engineer.  
Its task is to:  

- Input: Ingest a raw CV (PDF, DOCX, or TXT).  
- Process: Extract key information using an AI agent.  
- Output: Structured JSON that can be consumed by downstream systems.  

---

## 🚀 Feature: Specialized Skill Analyst
The **Skill Analyst Agent** plays the role of a subject matter expert.  
Its task is to:  

- Input: Structured JSON data from the CV Parser Agent.  
- Process: Analyze explicit skills, infer implicit skills from projects/experience, and identify transferable skills.  
- Output: Enhanced structured JSON with skill categorization and reasoning.  

---

## 🚀 Feature: Market Intelligence
The **Market Intelligence Agent** plays the role of a market researcher.  
Its task is to:  

- Input: The target role (e.g., "Senior AI Engineer").  
- Process: Use Tavily Search API to query job requirements and industry trends. Summarize in-demand skills and technologies.  
- Output: JSON object containing role, in-demand skills, and a concise market summary.  

### Example Output
```json
{
  "role": "Senior AI Engineer",
  "in_demand_skills": ["Python", "PyTorch", "TensorFlow", "MLOps", "AWS"],
  "summary": "Senior AI Engineers are expected to have strong Python skills, expertise in PyTorch/TensorFlow, experience with cloud platforms, and knowledge of MLOps best practices."
}
```
---

## ⚙️ Tech Stack
- FastAPI → REST API framework  
- Pydantic → Response schema validation & normalization  
- LangChain + OpenAI → AI agent for text parsing and reasoning  
- Tavily API → External search tool for market intelligence  
- PyPDF2 / python-docx → Text extraction utilities  
- pytest + httpx → Unit testing framework  

---

## 📂 Project Structure (simplified)
```json
sprout/
│── app/  
│   ├── src/  
│   │   ├── agents/  
│   │   │   ├── cv_parser.py        # AI CV Parser Agent  
│   │   │   ├── skill_analyst.py    # AI Skill Analyst Agent  
│   │   │   └── market_intel.py     # Market Intelligence Agent  
│   │   ├── utils/  
│   │   │   └── extractor.py        # Extractor for PDF/DOCX/TXT  
│   │   └── schemas/  
│   │       ├── cv_parser.py        # Schema for CV response  
│   │       ├── skill_analysis.py   # Schema for Skill Analyst response  
│   │       └── market_intel.py     # Schema for Market Intelligence response  
│   ├── main.py                     # FastAPI entry point  
│── tests/  
│   ├── data/                       # Test CVs (pdf, docx, txt)  
│   ├── test_cv_parser.py           # Unit tests for CV parser  
│   ├── test_skill_analyst.py       # Unit tests for skill analyst  
│   └── test_market_intel.py        # Unit tests for market intelligence  
```
---

## ▶️ Running the Application
1. Install dependencies:
   poetry install

2. Set your API keys:
   export OPENAI_API_KEY=your_openai_key
   export TAVILY_API_KEY=your_tavily_key

3. Start the FastAPI server:
   uvicorn app.main:app --reload

4. Open Swagger UI for testing:
   http://127.0.0.1:8000/docs

Endpoints available:
- POST `/api/agent/cv-parser` → upload CV file and get structured JSON  
- POST `/api/agent/skill-analyst` → analyze structured CV JSON for skills  
- POST `/api/agent/market-intelligent` → query market demands for a given role  

---

## 📝 How to Get Tavily API Key
1. Go to https://tavily.com  
2. Sign up for a free account  
3. Navigate to **API Keys** in your dashboard  
4. Copy your key and add it to your environment:
   export TAVILY_API_KEY=your_tavily_key

---

## 🤔 Why Tavily API?
- **LangChain Native Integration** → Tavily has first-class support in LangChain, so it’s plug-and-play.  
- **Relevant Results** → Tavily is optimized for AI agent search, unlike generic search engines.  
- **AI-Oriented** → Results are structured (title, url, snippet), making them easier for LLMs to consume.  
- **Fallback Ready** → If quota runs out, it’s easy to replace with DuckDuckGo search as backup.  

This makes Tavily the most practical and professional choice for building the Market Intelligence Agent.  

---

## ✅ Testing
Unit tests are included for all agents.  

Run tests:
   pytest -v

Tests cover:
- CV Parser → parses PDF/DOCX/TXT into JSON  
- Skill Analyst → analyzes explicit/implicit/transferable skills  
- Market Intelligence → queries (mocked) Tavily results and validates JSON output  