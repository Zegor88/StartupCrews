from typing import Type, List
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from openai import OpenAI
import os
from dotenv import load_dotenv
import pathlib
from agentops import record_tool

# Получаем путь к корневой директории проекта
ROOT_DIR = pathlib.Path(__file__).parent.parent.parent.parent.parent

# Загружаем переменные окружения из файла .env
load_dotenv(ROOT_DIR / ".env")

# Проверяем наличие ключа
if 'PERPLEXITY_API_KEY' not in os.environ:
    raise ValueError("PERPLEXITY_API_KEY не найден в переменных окружения")

class PerplexitySearchInput(BaseModel):
    """Input schema for Perplexity search."""
    query: str = Field(..., description="Search query")

class PerplexitySearchTool(BaseTool):
    name: str = "Perplexity Search Tool"
    description: str = (
        "This tool allows you to search for information through the Perplexity API. "
        "It is useful for searching and obtaining up-to-date information on a query."
        "Arguments: query - search query, input format: string"
    )
    args_schema: Type[BaseModel] = PerplexitySearchInput
    
    @record_tool('PerplexitySearch')
    def _run(self, query: str) -> str:
        client = OpenAI(
            api_key=os.environ['PERPLEXITY_API_KEY'],
            base_url="https://api.perplexity.ai"
        )
        
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an expert analyst specializing in market and business analysis. "
                    "Your task is to provide a detailed, structured answer based on up-to-date data. "
                    "Your analysis should be based on the latest (2024-2025) information and data available. "
                    "Include in the answer:\n"
                    "1. Key facts and statistics\n"
                    "2. Current trends and trends\n"
                    "3. Quantitative indicators (where applicable)\n"
                    "4. Links to reliable sources\n"
                    "Format: structured text with subheadings"
                )
            },
            {
                "role": "user",
                "content": query
            }
        ]

        try:
            response = client.chat.completions.create(
                model="llama-3.1-sonar-large-128k-online",
                messages=messages
            )
            
            answer_text = response.choices[0].message.content
            
            sources = "\n\nSources:\n"
            if hasattr(response, 'citations') and response.citations:
                for i, url in enumerate(response.citations, 1):
                    sources += f"{i}. {url}\n"
            else:
                sources += "Sources not found"
            
            return answer_text + sources

        finally:
            client.close()