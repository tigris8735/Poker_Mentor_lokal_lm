from aiogram import Router, types
from aiogram.filters import Command
from bot.services.ai_service import AIService

router = Router()
ai_service = AIService()

@router.message(Command("concept"))
async def concept_handler(message: types.Message):
    await message.answer("📚 Какую покерную концепцию объяснить? (например: 'позиция', 'блеф', 'пот оддсы')")

@router.message(Command("quiz"))
async def quiz_handler(message: types.Message):
    await message.answer("🎯 Выбери тему для квиза:\n- префлоп\n- постфлоп\n- блеф\n- чтение рук\n- банк менеджмент")

@router.message(lambda message: message.reply_to_message and 
                "покерную концепцию" in message.reply_to_message.text)
async def process_concept(message: types.Message):
    await message.answer("📖 Объясняю концепцию...")
    explanation = await ai_service.explain_concept(message.text)
    await message.answer(f"📚 {explanation}")

@router.message(lambda message: message.reply_to_message and 
                "тему для квиза" in message.reply_to_message.text)
async def process_quiz(message: types.Message):
    await message.answer("🎲 Создаю квиз...")
    quiz = await ai_service.generate_quiz(message.text)
    await message.answer(f"❓ {quiz}")