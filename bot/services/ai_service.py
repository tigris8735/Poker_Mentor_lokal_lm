import aiohttp
import json
import logging
from config.settings import LM_STUDIO_URL, AI_MODEL, MAX_TOKENS, TEMPERATURE
from .offline_ai import OfflineAIService

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        self.base_url = LM_STUDIO_URL
        self.model = AI_MODEL
        self.max_tokens = MAX_TOKENS
        self.temperature = TEMPERATURE
        self.headers = {"Content-Type": "application/json"}
        self.ai_available = True
        self.offline_ai = OfflineAIService()
        self.connection_checked = False
    
    async def check_connection(self):
        """Проверяет подключение к AI"""
        if self.connection_checked:
            return self.ai_available
            
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/models", timeout=5) as response:
                    if response.status == 200:
                        data = await response.json()
                        logger.info(f"LM Studio подключен. Модели: {[m['id'] for m in data.get('data', [])]}")
                        self.ai_available = True
                    else:
                        logger.warning(f"LM Studio вернул статус {response.status}")
                        self.ai_available = False
        except Exception as e:
            logger.warning(f"Не удалось подключиться к LM Studio: {e}")
            self.ai_available = False
            
        self.connection_checked = True
        return self.ai_available
    
    async def _make_request(self, prompt: str, system_message: str = None) -> str:
        """Универсальный метод для запросов к Qwen через LM Studio"""
        
        # Если AI недоступен, сразу возвращаем заглушку
        if not await self.check_connection():
            logger.info("Используем оффлайн-режим")
            return self.offline_ai.get_advice(prompt)
        
        messages = []
        
        if system_message:
            messages.append({"role": "system", "content": system_message})
        
        messages.append({"role": "user", "content": prompt})
        
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "stream": False
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/chat/completions",
                    headers=self.headers,
                    json=data,
                    timeout=15
                ) as response:
                    
                    response_text = await response.text()
                    logger.info(f"Raw AI response: {response_text[:200]}...")
                    
                    if response.status == 200:
                        result = await response.json()
                        
                        # Проверяем разные форматы ответа
                        if 'choices' in result and len(result['choices']) > 0:
                            return result['choices'][0]['message']['content']
                        elif 'content' in result:
                            return result['content']
                        elif 'message' in result:
                            return result['message']
                        else:
                            logger.error(f"Неожиданный формат ответа: {result}")
                            self.ai_available = False
                            return self.offline_ai.get_advice(prompt)
                    else:
                        logger.error(f"Ошибка API: {response.status} - {response_text}")
                        self.ai_available = False
                        return self.offline_ai.get_advice(prompt)
                        
        except Exception as e:
            logger.error(f"Ошибка подключения к AI: {e}")
            self.ai_available = False
            return self.offline_ai.get_advice(prompt)
    
    async def analyze_hand(self, hand_data: str) -> str:
        """Анализ покерной раздачи"""
        if not await self.check_connection():
            return self.offline_ai.analyze_hand(hand_data)
        
        system_message = """Ты профессиональный тренер по покеру Texas Hold'em. 
        Анализируй раздачи объективно, указывай на ошибки и давай конкретные рекомендации.
        Отвечай на русском языке кратко и по делу."""
        
        prompt = f"Проанализируй эту покерную раздачу и дай краткий разбор: {hand_data}"
        
        return await self._make_request(prompt, system_message)
    
    async def get_poker_advice(self, situation: str) -> str:
        """Совет по игровой ситуации"""
        if not await self.check_connection():
            return self.offline_ai.get_advice(situation)
        
        system_message = "Ты опытный покерный тренер. Дай четкий, практический совет по конкретной игровой ситуации. Отвечай на русском кратко."
        
        prompt = f"Покерная ситуация: {situation}. Дай профессиональный совет."
        
        return await self._make_request(prompt, system_message)
    
    async def explain_concept(self, concept: str) -> str:
        """Объяснение покерной концепции"""
        if not await self.check_connection():
            return f"Концепция: {concept}. В оффлайн-режиме используйте /analyze для анализа конкретных раздач."
        
        system_message = "Ты покерный ментор. Объясняй концепции понятно и с примерами. Отвечай на русском."
        
        prompt = f"Объясни покерную концепцию: {concept}"
        
        return await self._make_request(prompt, system_message)