from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type

class CharCounterInput(BaseModel):
    """Схема входных данных для инструмента подсчета символов"""
    text: str = Field(..., description="Текст для подсчета символов")

class CharCounterTool(BaseTool):
    name: str = "Character Counter Tool"
    description: str = "Подсчитывает количество символов в тексте, исключая пробелы"
    args_schema: Type[BaseModel] = CharCounterInput

    def _run(self, text: str) -> int:
        # Удаляем пробелы и подсчитываем символы
        return len(''.join(text.split()))