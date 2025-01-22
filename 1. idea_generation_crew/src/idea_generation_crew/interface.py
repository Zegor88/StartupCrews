import os
from dotenv import load_dotenv
import gradio as gr
from idea_generation_crew.crew import IdeaGenerationCrew

# Загрузка переменных окружения
load_dotenv()

def generate_ideas(topic):
    """
    Функция для генерации идей через CrewAI
    """
    try:
        inputs = {
            'topic': topic
        }
        result = IdeaGenerationCrew().crew().kickoff(inputs=inputs)
        
        # Проверяем тип результата и преобразуем соответственно
        if hasattr(result, 'content'):
            return result.content
        elif hasattr(result, 'output'):
            return result.output
        else:
            return str(result)
            
    except Exception as e:
        return f"Произошла ошибка: {str(e)}"

# Создаем простой интерфейс
iface = gr.Interface(
    fn=generate_ideas,
    inputs=gr.Textbox(
        label="Введите тему", 
        placeholder="например: AI Agents, Blockchain и т.д."
    ),
    outputs=gr.Textbox(label="Результат"),
    title="AI Система Генерации Идей",
    description="Введите тему для анализа и генерации инновационных идей."
)

if __name__ == "__main__":
    iface.launch(share=True) 