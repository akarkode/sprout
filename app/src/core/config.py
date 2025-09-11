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
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

settings = Settings()