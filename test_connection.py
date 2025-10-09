import asyncio
import aiohttp
import os
from config.settings import LM_STUDIO_URL

async def test_connection():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{LM_STUDIO_URL}/models") as response:
                if response.status == 200:
                    print("✅ Подключение к LM Studio успешно!")
                    models = await response.json()
                    print(f"Доступные модели: {models}")
                else:
                    print(f"❌ Ошибка HTTP: {response.status}")
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")

if __name__ == "__main__":
    asyncio.run(test_connection())