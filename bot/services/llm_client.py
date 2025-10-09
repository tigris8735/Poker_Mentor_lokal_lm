import aiohttp
import logging
import json
import asyncio
from config.settings import LM_STUDIO_URL, AI_MODEL

class LLMClient:
    def __init__(self):
        self.base_url = LM_STUDIO_URL
        self.model = AI_MODEL
        self.session = None
        
    async def get_session(self):
        if self.session is None:
            self.session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=120)
            )
        return self.session
        
    async def generate_response(self, prompt: str, max_tokens: int = 800) -> str:
        """
        Генерирует ответ от нейросети через LM Studio
        """
        try:
            session = await self.get_session()
            
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system", 
                        "content": """Ты - профессиональный покерный тренер с 10-летним опытом.
Отвечай ТОЛЬКО на вопросы, связанные с покером и азартными играми.
Будь точным, кратким и полезным. Используй профессиональную покерную терминологию.
Если вопрос не о покере - вежливо откажись отвечать, объяснив свою специализацию.
Всегда давай конкретные, практические советы по стратегии покера."""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": max_tokens,
                "temperature": 0.7,
                "top_p": 0.9,
                "stream": False
            }
            
            logging.info(f"🤖 Отправка запроса к LM Studio: {prompt[:100]}...")
            
            async with session.post(
                f"{self.base_url}/v1/chat/completions",
                json=payload,
                headers={"Content-Type": "application/json"}
            ) as response:
                
                if response.status == 200:
                    result = await response.json()
                    logging.info("✅ Успешный ответ от LM Studio")
                    
                    if "choices" in result and len(result["choices"]) > 0:
                        message_content = result["choices"][0]["message"]["content"]
                        logging.info(f"🤖 Ответ AI: {message_content[:200]}...")
                        return message_content.strip()
                    else:
                        logging.error(f"❌ Неверный формат ответа: {result}")
                        return "Извините, не удалось обработать ответ нейросети."
                        
                else:
                    error_text = await response.text()
                    logging.error(f"❌ Ошибка LM Studio: {response.status} - {error_text}")
                    return await self._try_completions_endpoint(prompt, max_tokens)
                    
        except aiohttp.ClientConnectorError as e:
            logging.error(f"❌ Ошибка подключения к LM Studio: {e}")
            return "Ошибка подключения к нейросети. Проверьте, запущен ли LM Studio."
        except asyncio.TimeoutError:
            logging.error("⏰ Таймаут подключения к LM Studio")
            return "Нейросеть не отвечает. Попробуйте позже."
        except Exception as e:
            logging.error(f"❌ Неожиданная ошибка: {str(e)}")
            return "Произошла непредвиденная ошибка."
    
    async def _try_completions_endpoint(self, prompt: str, max_tokens: int) -> str:
        """
        Альтернативный метод через эндпоинт completions
        """
        try:
            session = await self.get_session()
            
            payload = {
                "model": self.model,
                "prompt": f"Ты покерный тренер. Ответь на вопрос: {prompt}",
                "max_tokens": max_tokens,
                "temperature": 0.7,
                "stream": False
            }
            
            logging.info("🔄 Пробуем эндпоинт /v1/completions...")
            
            async with session.post(
                f"{self.base_url}/v1/completions",
                json=payload,
                headers={"Content-Type": "application/json"}
            ) as response:
                
                if response.status == 200:
                    result = await response.json()
                    
                    if "choices" in result and len(result["choices"]) > 0:
                        text_response = result["choices"][0]["text"]
                        logging.info(f"✅ Ответ через completions: {text_response[:200]}...")
                        return text_response.strip()
                    else:
                        return "Нейросеть вернула пустой ответ."
                else:
                    error_text = await response.text()
                    logging.error(f"❌ Ошибка completions эндпоинта: {error_text}")
                    return "Оба эндпоинта нейросети недоступны."
                    
        except Exception as e:
            logging.error(f"❌ Ошибка альтернативного эндпоинта: {e}")
            return "Все методы подключения к нейросети не сработали."
            
    async def close(self):
        if self.session:
            await self.session.close()

# Глобальный экземпляр
llm_client = LLMClient()