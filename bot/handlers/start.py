from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer(
        "🤖 Привет! Я покерный помощник с AI.\n\n"
        "Доступные команды:\n"
        "/ask [вопрос] - задать вопрос AI\n"
        "/analysis [раздача] - анализ покерной раздачи\n\n"
        "Или просто напишите вопрос о покере!"
    )