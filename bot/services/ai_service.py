import aiohttp
import json
from config.settings import LM_STUDIO_URL, AI_MODEL, MAX_TOKENS, TEMPERATURE

class AIService:
    def __init__(self):
        self.base_url = LM_STUDIO_URL
        self.model = AI_MODEL
        self.max_tokens = MAX_TOKENS
        self.temperature = TEMPERATURE
        self.headers = {
            "Content-Type": "application/json"
        }
    
    async def _make_request(self, prompt: str, system_message: str = None) -> str:
        """Универсальный метод для запросов к Qwen через LM Studio"""
        
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
                    timeout=30  # Уменьшаем таймаут для быстрой модели
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result['choices'][0]['message']['content']
                    else:
                        error_text = await response.text()
                        return f"Ошибка API: {response.status} - {error_text}"
            except Exception as e:
                return f"Ошибка соединения: {str(e)}"
    
    async def analyze_hand(self, hand_data: str) -> str:
        """Анализ покерной раздачи - оптимизировано для Qwen"""
        system_message = """Ты покерный тренер. Отвечай кратко и по делу. 
        Формат ответа: 
        1. Оценка руки 
        2. Основные ошибки 
        3. Рекомендации
        Максимум 3 предложения на пункт."""
        
        prompt = f"""
        Раздача: {hand_data}
        Проанализируй кратко:
        """
        
        return await self._make_request(prompt, system_message)
    
    async def get_poker_advice(self, situation: str) -> str:
        """Совет по игровой ситуации - оптимизировано для Qwen"""
        system_message = "Дай короткий практический совет по покеру. 2-3 предложения."
        
        prompt = f"Ситуация: {situation}. Какой твой совет?"
        
        return await self._make_request(prompt, system_message)
    
    async def explain_concept(self, concept: str) -> str:
        """Объяснение покерной концепции - оптимизировано для Qwen"""
        system_message = "Объясни покерную концепцию просто и понятно. 3-4 предложения."
        
        prompt = f"Объясни: {concept}"
        
        return await self._make_request(prompt, system_message)
    
    async def generate_quiz(self, topic: str) -> str:
        """Создание покерного квиза - оптимизировано для Qwen"""
        system_message = "Создай один вопрос по покеру с 4 вариантами ответов и правильным ответом."
        
        prompt = f"Тема: {topic}. Создай вопрос с вариантами A,B,C,D и укажи правильный ответ."
        
        return await self._make_request(prompt, system_message)