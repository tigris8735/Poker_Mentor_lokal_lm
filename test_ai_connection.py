import asyncio
import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()

async def test_ai():
    url = os.getenv('LM_STUDIO_URL') + "/chat/completions"
    
    test_data = {
        "model": "qwen3-4b-2507",
        "messages": [
            {"role": "system", "content": "Ты покерный тренер."},
            {"role": "user", "content": "Скажи привет на русском"}
        ],
        "temperature": 0.3,
        "max_tokens": 50
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=test_data, timeout=10) as response:
                if response.status == 200:
                    result = await response.json()
                    print("✅ AI работает!")
                    print(f"Ответ: {result['choices'][0]['message']['content']}")
                else:
                    print(f"❌ Ошибка AI: {response.status}")
                    print(await response.text())
    except Exception as e:
        print(f"❌ Не удалось подключиться к AI: {e}")

if __name__ == "__main__":
    asyncio.run(test_ai())