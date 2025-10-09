import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from bot.services.ai_service import AIService

async def test_ai():
    ai = AIService()
    
    print("🔍 Проверяем подключение к AI...")
    is_connected = await ai.check_connection()
    print(f"Подключение: {'✅' if is_connected else '❌'}")
    
    if is_connected:
        print("\n🧪 Тестируем запрос к AI...")
        try:
            response = await ai.get_poker_advice("У меня пара тузов на префлопе")
            print(f"✅ Ответ AI:\n{response}")
        except Exception as e:
            print(f"❌ Ошибка: {e}")
    else:
        print("\n🤖 Тестируем оффлайн-режим...")
        response = await ai.get_poker_advice("У меня пара тузов на префлопе")
        print(f"Оффлайн ответ:\n{response}")

if __name__ == "__main__":
    asyncio.run(test_ai())