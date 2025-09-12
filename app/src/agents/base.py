from __future__ import annotations

import json
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from app.src.core.config import settings


class AIBaseAgent:
    def __init__(self, model: str = "gpt-4o-mini"):
        self.llm = ChatOpenAI(model=model, api_key=settings.OPENAI_KEY)

    def run(self, prompt_template: str, variables: dict) -> dict:
        """
        Run LLM with given prompt template and variables.
        - prompt_template: string template for ChatPromptTemplate
        - variables: dict of key-value pairs to inject into the prompt
          e.g., {"cv_text": "...", "role": "...", "search_results": "..."}
        """
        prompt = ChatPromptTemplate.from_template(prompt_template)
        chain = prompt | self.llm
        response = chain.invoke(variables)

        try:
            return json.loads(response.content)
        except Exception as e:
            return {"error": str(e), "raw_output": response.content}
