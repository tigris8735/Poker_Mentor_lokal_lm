from aiogram import Router, types
from aiogram.filters import Command
from bot.services.ai_service import ai_service

router = Router()

@router.message(Command("ask"))
async def ask_ai_handler(message: types.Message):
    """Обработчик вопросов к AI"""
    question = message.text.replace('/ask', '').strip()
    
    if not question:
        await message.answer("Пожалуйста, задайте вопрос после команды /ask")
        return
    
    # Показываем что бот печатает
    await message.bot.send_chat_action(message.chat.id, "typing")
    
    # Получаем ответ от AI
    answer = await ai_service.get_ai_response(question)
    
    await message.answer(f"🤖 AI Помощник:\n\n{answer}")

@router.message(Command("analysis"))
async def analyze_hand_handler(message: types.Message):
    """Анализ раздачи с помощью AI"""
    hand_description = message.text.replace('/analysis', '').strip()
    
    if not hand_description:
        await message.answer("Опишите раздачу для анализа после команды /analysis")
        return
    
    await message.bot.send_chat_action(message.chat.id, "typing")
    
    prompt = f"Проанализируй эту покерную раздачу и дай рекомендации: {hand_description}"
    analysis = await ai_service.get_ai_response(prompt)
    
    await message.answer(f"📊 Анализ раздачи:\n\n{analysis}")