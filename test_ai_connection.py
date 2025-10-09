import asyncio
import sys
import os

# Добавляем корневую директорию в путь
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from bot.services.llm_client import llm_client

async def test_ai():
    print("🧪 Тестирование подключения к AI...")
    
    test_prompts = [
        "Привет! Как дела?",
        "Какие карты лучше всего для старта в техасском холдеме?",
        "Объясни базовую стратегию префлопа"
    ]
    
    for prompt in test_prompts:
        print(f"\n📤 Вопрос: {prompt}")
        response = await llm_client.generate_response(prompt, 200)
        print(f"📥 Ответ: {response}")
        print("─" * 50)

async def main():
    try:
        await test_ai()
    finally:
        await llm_client.close()

if __name__ == "__main__":
    asyncio.run(main())