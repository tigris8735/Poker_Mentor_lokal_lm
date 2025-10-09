from aiogram import Router, types
from aiogram.filters import Command
from bot.services.database import Database

router = Router()
db = Database()

@router.message(Command("start"))
async def start_handler(message: types.Message):
    user = db.get_or_create_user(
        message.from_user.id,
        message.from_user.username,
        message.from_user.first_name,
        message.from_user.last_name
    )
    
    welcome_text = f"""
    🃏 Добро пожаловать в Poker_mentor, {message.from_user.first_name}!

    Доступные команды:
    /start - Начать работу
    /game - Начать игру с AI
    /analyze - Проанализировать раздачу
    /advice - Получить совет по игре
    /stats - Моя статистика

    Развивай свои покерные навыки!
    """
    
    await message.answer(welcome_text)