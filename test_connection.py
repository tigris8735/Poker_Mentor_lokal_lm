import asyncio
import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()

async def test_connection():
    url = os.getenv('LM_STUDIO_URL', 'http://localhost:1234/v1') + "/models"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    print("✅ Подключение к LM Studio успешно!")
                    print(f"Доступные модели: {[m['id'] for m in data['data']]}")
                else:
                    print(f"❌ Ошибка: {response.status}")
    except Exception as e:
        print(f"❌ Не удалось подключиться к {url}")
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    asyncio.run(test_connection())