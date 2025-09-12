from __future__ import annotations

import json
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from app.src.core.config import settings


class AIBaseAgent:
    def __init__(self, model: str = "gpt-4o-mini"):
        self.llm = ChatOpenAI(model=model, api_key=settings.OPENAI_KEY)

    def run(self, prompt_template: str, variable_key: str, variable_value: str) -> dict:
        """
        Run LLM with given prompt template and variable.
        - prompt_template: string template for ChatPromptTemplate
        - variable_key: placeholder name in prompt (e.g., 'cv_text' or 'cv_data')
        - variable_value: value to inject into the prompt
        """
        prompt = ChatPromptTemplate.from_template(prompt_template)
        chain = prompt | self.llm
        response = chain.invoke({variable_key: variable_value})

        try:
            print(response.content)
            return json.loads(response.content)
        except Exception as e:
            return {"error": str(e), "raw_output": response.content}
