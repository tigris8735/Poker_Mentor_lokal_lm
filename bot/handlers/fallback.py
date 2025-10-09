from aiogram import Router, types
from bot.services.ai_service import ai_service

router = Router()

@router.message()
async def general_handler(message: types.Message):
    """Обработчик всех сообщений"""
    text = message.text.strip()
    
    if not text or text.startswith('/'):
        return
    
    # Если сообщение достаточно длинное, считаем его вопросом
    if len(text) > 5:
        await message.bot.send_chat_action(message.chat.id, "typing")
        response = await ai_service.get_ai_response(text)
        await message.answer(f"🎯 AI помощник:\n\n{response}")