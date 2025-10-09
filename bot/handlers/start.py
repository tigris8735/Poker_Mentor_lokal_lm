from aiogram import Router, types
from aiogram.filters import Command
from bot.services.database import Database
from bot.services.ai_service import AIService

router = Router()
db = Database()
ai_service = AIService()

@router.message(Command("start"))
async def start_handler(message: types.Message):
    user = db.get_or_create_user(
        message.from_user.id,
        message.from_user.username,
        message.from_user.first_name,
        message.from_user.last_name
    )
    
    # Проверяем статус AI
    ai_status = "✅ Доступен" if ai_service.ai_available else "❌ Временные заглушки"
    
    welcome_text = f"""
    🃏 Добро пожаловать в Poker_mentor, {message.from_user.first_name}!

    Статус AI: {ai_status}

    Доступные команды:
    /start - Начать работу
    /game - Начать игру с AI
    /analyze - Проанализировать раздачу
    /advice - Получить совет по игре
    /stats - Моя статистика

    Развивай свои покерные навыки!
    """
    
    await message.answer(welcome_text)

@router.message(Command("status"))
async def status_handler(message: types.Message):
    """Показывает статус системы"""
    ai_status = "✅ Доступен" if ai_service.ai_available else "❌ Временные заглушки"
    
    status_text = f"""
    📊 Статус системы:

    🤖 AI: {ai_status}
    💾 База данных: ✅ Активна
    🎮 Игровой движок: ✅ Активен

    Используйте команды для взаимодействия!
    """
    
    await message.answer(status_text)