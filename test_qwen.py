import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from bot.services.ai_service import AIService

async def test_qwen():
    ai = AIService()
    print("Тестируем Qwen...")
    
    # Тест 1: Короткий совет
    response = await ai.get_poker_advice("У меня пара королей на префлопе")
    print("Совет:", response)
    
    # Тест 2: Анализ раздачи
    hand = "Префлоп: AKs, рейз 3BB, колл от 2 игроков. Флоп: A-9-2 радужный."
    analysis = await ai.analyze_hand(hand)
    print("Анализ:", analysis)

if __name__ == "__main__":
    asyncio.run(test_qwen())