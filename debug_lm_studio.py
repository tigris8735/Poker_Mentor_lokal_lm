import asyncio
import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()

async def debug_lm_studio():
    base_url = os.getenv('LM_STUDIO_URL', 'http://localhost:1234/v1').rstrip('/')
    
    print(f"🔍 Диагностика LM Studio: {base_url}")
    print("=" * 50)
    
    # Тестируем разные endpoint'ы
    endpoints = [
        '',
        '/models',
        '/v1/models',
        '/chat/completions', 
        '/v1/chat/completions',
        '/completions',
        '/v1/completions'
    ]
    
    async with aiohttp.ClientSession() as session:
        for endpoint in endpoints:
            url = f"{base_url}{endpoint}"
            print(f"\n📡 Тестируем: {url}")
            
            try:
                if endpoint in ['', '/models', '/v1/models']:
                    # GET запрос
                    async with session.get(url, timeout=5) as response:
                        print(f"   Status: {response.status}")
                        if response.status == 200:
                            data = await response.json()
                            print(f"   ✅ Успех: {data}")
                        else:
                            print(f"   ❌ Ошибка: {await response.text()}")
                else:
                    # POST запрос
                    test_data = {
                        "model": "test-model",
                        "messages": [{"role": "user", "content": "Hello"}],
                        "max_tokens": 10
                    }
                    
                    async with session.post(url, json=test_data, timeout=5) as response:
                        print(f"   Status: {response.status}")
                        if response.status == 200:
                            data = await response.json()
                            print(f"   ✅ Успех")
                        else:
                            error_text = await response.text()
                            print(f"   ❌ Ошибка: {error_text}")
                            
            except Exception as e:
                print(f"   💥 Исключение: {e}")

if __name__ == "__main__":
    asyncio.run(debug_lm_studio())