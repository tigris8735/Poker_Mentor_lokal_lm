import asyncio
import sys
import os

# Добавляем корневую директорию в путь
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from bot.services.llm_client import llm_client

async def test_ai():
    print("🧪 Тестирование подключения к AI...")
    
    test_prompt = "Какие карты лучше всего для старта в техасском холдеме?"
    
    print(f"📤 Вопрос: {test_prompt}")
    response = await llm_client.generate_response(test_prompt, 500)
    print(f"📥 Ответ: {response}")
    print("─" * 50)

async def main():
    try:
        await test_ai()
    finally:
        await llm_client.close()

if __name__ == "__main__":
    asyncio.run(main())