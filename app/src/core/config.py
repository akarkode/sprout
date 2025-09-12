from __future__ import annotations

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    OPENAI_KEY: str = ""
    TAVILY_API_KEY: str = ""
    CV_PARSER_PROMPT: str = """
            You are an expert CV parser. 
            Extract the following fields from the text and return them in JSON format:

            {{
            "name": "string",
            "email": "string",
            "phone": "string",
            "education": [
                {{
                "degree": "string",
                "institution": "string",
                "year": "string"
                }}
            ],
            "experience": [
                {{
                "position": "string",
                "company": "string",
                "years": "string",
                "description": "string"
                }}
            ],
            "skills": ["string", "string"],
            "projects": [
                {{
                "title": "string",
                "description": "string",
                "technologies": ["string", "string"]
                }}
            ]
            }}

            Return only a valid JSON object, no explanation, no markdown.

            CV Text:
            {cv_text}
        """
    SKILL_ANALYST_PROMPT: str = """
            You are an expert skill analyst.

            Task: Analyze the following structured CV data to identify skills.
            - explicit_skills: directly listed in the CV.
            - implicit_skills: not listed, but can be inferred from experience/projects.
            - transferable_skills: skills that are applicable across domains.
            - description: explanation of why you inferred certain implicit and transferable skills.

            Return only a valid JSON object in the following format:
            {{
            "explicit_skills": [],
            "implicit_skills": [],
            "transferable_skills": [],
            "descriptions": []
            }}

            No additional explanation, no markdown, only the JSON object.

            CV Data:
            {cv_data_json}
        """
    MARKETING_INTELEGENT_PROMPT: str = """
            You are a market intelligence analyst.
            Task: Analyze the search results about the role "{role}".
            
            Extract:
            - A list of in-demand skills and technologies.
            - A concise summary (3-5 sentences) of market expectations.

            Always return ONLY valid JSON:
            {{
            "role": "{role}",
            "in_demand_skills": [],
            "summary": ""
            }}
            No additional explanation, no markdown, only the JSON object.
            Search Results:
            {search_results}
        """
    REPORT_PROMPT: str = """
            You are a strategist and communicator AI.
            Your job is to combine candidate CV data, skill analysis, and market intelligence 
            into a professional and engaging Markdown report.

            Make the report:
            - Well structured with clear headings and subheadings.
            - Use bullet points and numbered lists where appropriate.
            - Friendly but professional tone (not boring).
            - Always return ONLY valid Markdown text.

            Sections to include:
            1. **Candidate Summary** (name, email, key skills from CV).
            2. **Skill Analysis** (explicit, implicit, transferable skills).
            3. **Market Analysis** (in-demand skills & trends for the role).
            4. **Skill Gap** (compare candidate skills vs market demands).
            5. **Upskilling Plan** (personalized learning roadmap).

            Inputs:
            - Candidate Info (from CV Parser):
            {candidate_info}

            - Skill Analysis (from Skill Analyst Agent):
            {skill_analysis}

            - Market Analysis (from Market Intelligence Agent):
            {market_analysis}

            Output:
            A well-formatted Markdown report. No additional explanation, only markdown plaintext.
        """

settings = Settings(_env_file='.env')