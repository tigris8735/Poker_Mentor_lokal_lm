import aiohttp
import json
import logging
from config.settings import LM_STUDIO_URL, AI_MODEL, MAX_TOKENS, TEMPERATURE

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        self.base_url = LM_STUDIO_URL
        self.model = AI_MODEL
        self.max_tokens = MAX_TOKENS
        self.temperature = TEMPERATURE
        self.headers = {
            "Content-Type": "application/json"
        }
        self.ai_available = True
    
    async def _make_request(self, prompt: str, system_message: str = None) -> str:
        """Универсальный метод для запросов к Qwen через LM Studio"""
        
        # Если AI недоступен, сразу возвращаем заглушку
        if not self.ai_available:
            return self._get_fallback_response(prompt)
        
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
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    f"{self.base_url}/chat/completions",
                    headers=self.headers,
                    json=data,
                    timeout=10
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result['choices'][0]['message']['content']
                    else:
                        logger.warning(f"AI server returned status {response.status}")
                        self.ai_available = False
                        return self._get_fallback_response(prompt)
            except Exception as e:
                logger.error(f"AI connection failed: {e}")
                self.ai_available = False
                return self._get_fallback_response(prompt)
    
    def _get_fallback_response(self, prompt: str) -> str:
        """Возвращает заглушку когда AI недоступен"""
        if "анализ" in prompt.lower() or "раздач" in prompt.lower():
            return """🔧 AI временно недоступен. Вот базовый анализ:

1. Оцените силу своей руки
2. Учитывайте позицию за столом  
3. Следите за размером банка
4. Наблюдайте за действиями оппонентов

Для точного анализа дождитесь восстановления подключения к AI."""
        
        elif "совет" in prompt.lower() or "ситуац" in prompt.lower():
            return """💡 Общий покерный совет:

• Играйте тайтово-агрессивно
• Учитывайте позицию
• Управляйте банкроллом
• Анализируйте оппонентов

AI скоро будет доступен для персонализированных советов!"""
        
        else:
            return "🤖 AI временно недоступен. Пожалуйста, попробуйте позже."
    
    async def analyze_hand(self, hand_data: str) -> str:
        """Анализ покерной раздачи"""
        system_message = """Ты покерный тренер. Отвечай кратко и по делу."""
        
        prompt = f"Раздача: {hand_data}. Проанализируй кратко:"
        
        return await self._make_request(prompt, system_message)
    
    async def get_poker_advice(self, situation: str) -> str:
        """Совет по игровой ситуации"""
        system_message = "Дай короткий практический совет по покеру."
        
        prompt = f"Ситуация: {situation}. Какой твой совет?"
        
        return await self._make_request(prompt, system_message)