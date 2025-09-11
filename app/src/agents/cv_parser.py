from __future__ import annotations

import json
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

from app.src.core.config import settings


class AICVParser:
    def __init__(self, model_name: str = "gpt-4o-mini"):
        """
        AICVParser: Agent for parsing CVs using OpenAI API via LangChain.

        Why is `gpt-4o-mini` the default choice?
        - CV parsing requires structured extraction (JSON) and light reasoning,
          which a small but capable model can handle well.
        - CVs are typically short (2–5 pages), so large context windows are not mandatory.
        - `gpt-4o-mini` is very cost-efficient (~$0.15 / 1M input tokens),
          making it ideal for batch-processing multiple CVs.
        - It has low latency, making it suitable for real-time parsing in a web app.

        When to consider other models?
        - `gpt-4o`: if handling more complex documents (e.g., portfolios, 
          research papers) where stronger reasoning is required, 
          but note that it’s more expensive.
        - `gpt-3.5-turbo`: cheaper, but often less consistent in producing strict JSON output.
        """
        self.llm = ChatOpenAI(model=model_name, api_key=settings.OPENAI_KEY)
        self.prompt = ChatPromptTemplate.from_template(settings.CV_PARSER_PROMPT)



    def parse(self, cv_text: str) -> dict:
        """Parses CV text into a structured JSON object."""
        chain = self.prompt | self.llm
        response = chain.invoke({"cv_text": cv_text})

        try:
            return json.loads(response.content)
        except json.JSONDecodeError:
            return {"error": "Invalid JSON", "raw_output": response.content}
