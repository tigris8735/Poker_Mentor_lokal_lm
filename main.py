import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from config.settings import BOT_TOKEN
from bot.services.llm_client import llm_client
from bot.services.database import Database

# Импорты роутеров
from bot.handlers.start import router as start_router
from bot.handlers.ai_chat import router as ai_chat_router
from bot.handlers.poker_game import router as poker_game_router
from bot.handlers.analysis import router as analysis_router
from bot.handlers.fallback import router as fallback_router

logging.basicConfig(level=logging.INFO)

# Инициализация
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
db = Database()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    
    db.save_user(user_id, username, first_name)
    
    await message.answer(
        "🤖 <b>Добро пожаловать в Poker Mentor AI 2.0!</b>\n\n"
        "🎮 <b>Новые возможности:</b>\n"
        "• Игра 1x1 с AI (/poker)\n"
        "• Умный AI-помощник (/ask)\n"
        "• Расширенный анализ (/ask_advanced)\n"
        "• Анализ раздач (/analysis)\n\n"
        "💡 <b>Основные команды:</b>\n"
        "/poker - Играть в покер с AI\n"
        "/ask - Задать вопрос AI\n"
        "/analysis - Анализ раздачи\n"
        "/help - Помощь\n\n"
        "🚀 <b>Начните с игры /poker или задайте вопрос /ask!</b>",
        parse_mode="HTML"
    )

# Регистрируем все роутеры
dp.include_router(start_router)
dp.include_router(ai_chat_router)
dp.include_router(poker_game_router)
dp.include_router(analysis_router)
dp.include_router(fallback_router)

async def main():
    db.init_db()
    
    bot_info = await bot.get_me()
    logging.info(f"✅ Бот запущен: {bot_info.full_name}")
    
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"❌ Ошибка: {e}")
    finally:
        await llm_client.close()
        db.close()
        logging.info("👋 Бот остановлен")

if __name__ == "__main__":
    asyncio.run(main())