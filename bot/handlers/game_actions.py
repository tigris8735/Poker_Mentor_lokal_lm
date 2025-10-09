from aiogram import Router, types
from bot.services.ai_service import ai_service

router = Router()

@router.message()
async def general_questions_handler(message: types.Message):
    """Обработчик общих вопросов о покере"""
    text = message.text.lower()
    
    # Если сообщение похоже на вопрос о покере
    poker_keywords = ['покер', 'раздача', 'блеф', 'стейк', 'флоп', 'терн', 'ривер', 'колл', 'рейз', 'фолд']
    
    if any(keyword in text for keyword in poker_keywords) and len(text) > 10:
        await message.bot.send_chat_action(message.chat.id, "typing")
        
        response = await ai_service.get_ai_response(
            f"Вопрос о покере: {message.text}",
            "Ты - опытный покерный тренер. Дай краткий и полезный ответ."
        )
        
        await message.answer(f"🎯 Совет от AI:\n\n{response}")