from __future__ import annotations

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    OPENAI_KEY: str = ""
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
settings = Settings(_env_file='.env')