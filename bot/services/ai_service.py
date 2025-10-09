import aiohttp
import json
from config.settings import LM_STUDIO_URL, AI_MODEL

class AIService:
    def __init__(self):
        self.base_url = LM_STUDIO_URL
        self.model = AI_MODEL
        self.headers = {
            "Content-Type": "application/json"
        }
    
    async def _make_request(self, prompt: str, system_message: str = None) -> str:
        """Универсальный метод для запросов к DeepSeek через LM Studio"""
        
        messages = []
        
        if system_message:
            messages.append({"role": "system", "content": system_message})
        
        messages.append({"role": "user", "content": prompt})
        
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 1024,
            "stream": False
        }
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    f"{self.base_url}/chat/completions",
                    headers=self.headers,
                    json=data,
                    timeout=60
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
        """Анализ покерной раздачи"""
        system_message = """Ты профессиональный тренер по покеру Texas Hold'em. 
        Анализируй раздачи объективно, указывай на ошибки и давай конкретные рекомендации.
        Отвечай на русском языке."""
        
        prompt = f"""
        Проанализируй эту покерную раздачу и дай подробный разбор:

        {hand_data}

        Структура анализа:
        1. Предварительная оценка руки
        2. Анализ действий на каждой улице
        3. Оценка решений игрока
        4. Конкретные рекомендации на будущее

        Будь строгим но конструктивным тренером.
        """
        
        return await self._make_request(prompt, system_message)
    
    async def get_poker_advice(self, situation: str) -> str:
        """Совет по игровой ситуации"""
        system_message = """Ты опытный покерный тренер. Дай четкий, практический совет 
        по конкретной игровой ситуации. Отвечай на русском."""
        
        prompt = f"""
        Покерная ситуация: {situation}

        Дай профессиональный совет по этой ситуации. Разбери:
        - Оптимальную стратегию
        - Распространенные ошибки
        - Как улучшить игру в подобных спотах
        """
        
        return await self._make_request(prompt, system_message)
    
    async def explain_concept(self, concept: str) -> str:
        """Объяснение покерной концепции"""
        system_message = """Ть покерный ментор. Объясняй концепции понятно и с примерами.
        Отвечай на русском."""
        
        prompt = f"""
        Объясни покерную концепцию: {concept}

        В объяснении включи:
        - Простое определение
        - Практические примеры
        - Как применять в игре
        - Частые ошибки
        """
        
        return await self._make_request(prompt, system_message)
    
    async def generate_quiz(self, topic: str) -> str:
        """Создание покерного квиза"""
        system_message = """Ты создаешь обучающие покерные квизы. 
        Создавай реалистичные игровые ситуации с вариантами ответов."""
        
        prompt = f"""
        Создай покерный квиз на тему: {topic}

        Формат:
        Вопрос: [реалистичная игровая ситуация]
        Варианты ответов: A, B, C, D
        Правильный ответ: [буква]
        Объяснение: [подробное объяснение почему этот ответ правильный]

        Сделай 1 качественный вопрос.
        """
        
        return await self._make_request(prompt, system_message)