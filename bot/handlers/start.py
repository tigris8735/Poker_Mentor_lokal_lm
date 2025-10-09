from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("help"))
async def help_handler(message: types.Message):
    await message.answer(
        "🆘 <b>Помощь по командам:</b>\n\n"
        "/start - Начало работы\n"
        "/poker - Игра в покер с AI\n"
        "/ask - Вопрос к AI-помощнику\n"
        "/ask_advanced - Расширенный вопрос\n"
        "/analysis - Анализ покерной раздачи\n"
        "/stats - Ваша статистика\n"
        "/game_stats - Статистика игр\n"
        "/clear_context - Очистить контекст\n"
        "/end_game - Завершить текущую игру\n"
        "/help - Эта справка",
        parse_mode="HTML"
    )