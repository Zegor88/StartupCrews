from typing import Type, List
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from openai import OpenAI
import os

class PerplexitySearchInput(BaseModel):
    """Input schema for Perplexity search."""
    query: str = Field(..., description="Search query")
    domains: List[str] = Field(
        default=[],
        description="List of domains to filter search results"
    )

class PerplexitySearchTool(BaseTool):
    name: str = "Perplexity Search Tool"
    description: str = (
        "This tool allows you to search for information through the Perplexity API with the ability to filter by domains. "
        "It is useful for searching and obtaining up-to-date information on a query."
        "Arguments: query - search query, input format: string"
    )
    args_schema: Type[BaseModel] = PerplexitySearchInput

    def _run(self, query: str, domains: List[str]) -> str:
        client = OpenAI(
            api_key=os.environ['PERPLEXITY_API_KEY'],
            base_url="https://api.perplexity.ai"
        )
        
        # Формируем поисковый запрос с фильтрацией по доменам
        domain_filter = " OR ".join(f"site:{domain}" for domain in domains)
        search_query = f"{domain_filter} {query}"
        
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an expert research assistant focused on providing comprehensive, "
                    "factual information about emerging technologies, market trends, and innovations in 2025. "
                     )
            },
            {
                "role": "user",
                "content": search_query
            }
        ]

        try:
            response = client.chat.completions.create(
                model="llama-3.1-sonar-large-128k-online",
                messages=messages
            )
            
            # Получаем основной текст ответа
            answer_text = response.choices[0].message.content
            
            # Формируем список источников
            sources = "\n\nSources:\n"
            if hasattr(response, 'citations') and response.citations:
                for i, url in enumerate(response.citations, 1):
                    sources += f"{i}. {url}\n"
            else:
                sources += "Sources not found"
            
            # Возвращаем объединенный результат
            return answer_text + sources

        finally:
            # Закрываем клиент после использования
            client.close()