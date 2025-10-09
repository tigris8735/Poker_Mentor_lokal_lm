import logging
from bot.services.llm_client import llm_client

class AIService:
    def __init__(self):
        self.llm_client = llm_client
    
    async def get_ai_response(self, prompt: str, context: str = "") -> str:
        """
        Получает ответ от AI для покерных вопросов
        """
        try:
            # Добавляем покерный контекст если нужно
            if context:
                full_prompt = f"Контекст: {context}\n\nВопрос: {prompt}"
            else:
                full_prompt = f"Покерный вопрос: {prompt}"
            
            response = await self.llm_client.generate_response(full_prompt)
            return response if response else "Нейросеть временно недоступна. Попробуйте позже."
            
        except Exception as e:
            logging.error(f"❌ AI Service error: {str(e)}")
            return "Произошла ошибка при обращении к нейросети."

# Глобальный экземпляр
ai_service = AIService()