from aiogram import Router, types
from bot.services.ai_service import ai_service

router = Router()

@router.message()
async def fallback_handler(message: types.Message):
    """Обработчик всех сообщений не попавших в другие хендлеры"""
    text = message.text.strip()
    
    if not text or text.startswith('/'):
        return
    
    # Отвечаем только на достаточно длинные сообщения
    if len(text) > 10:
        await message.answer("💭 Анализирую ваш вопрос...")
        response = await ai_service.get_ai_response(text)
        await message.answer(f"🎯 <b>Poker Mentor:</b>\n\n{response}", parse_mode="HTML")