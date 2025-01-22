import os
from dotenv import load_dotenv

def test_environment():
    # Загружаем переменные окружения
    load_dotenv()
    
    # Проверяем наличие ключей
    keys = [
        "PERPLEXITY_API_KEY",
        "LANGTRACE_API_KEY",
        "AGENTOPS_API_KEY"
    ]
    
    for key in keys:
        value = os.getenv(key)
        if value:
            print(f"✅ {key} успешно загружен")
        else:
            print(f"❌ {key} не найден")

if __name__ == "__main__":
    test_environment() 