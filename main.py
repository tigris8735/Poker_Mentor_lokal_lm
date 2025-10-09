import asyncio
import logging
from aiogram import Bot, Dispatcher
from config.settings import BOT_TOKEN

# Импорты роутеров
from bot.handlers.start import router as start_router
from bot.handlers.game import router as game_router
from bot.handlers.analysis import router as analysis_router
from bot.handlers.learning import router as learning_router
from bot.handlers.game_actions import router as game_actions_router
from bot.handlers.fallback import router as fallback_router

from bot.services.database import Database
from bot.services.llm_client import llm_client

logging.basicConfig(level=logging.INFO)

async def main():
    # Инициализация БД
    db = Database()
    db.init_db()
    
    # Инициализация бота
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    # Регистрация ВСЕХ роутеров
    dp.include_router(start_router)
    dp.include_router(game_router)
    dp.include_router(analysis_router)
    dp.include_router(learning_router)
    dp.include_router(game_actions_router)
    dp.include_router(fallback_router)
    
    logging.info("🤖 Бот запущен с интеграцией LM Studio AI")
    
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"❌ Ошибка запуска бота: {e}")
    finally:
        await llm_client.close()
        logging.info("👋 Бот остановлен")

if __name__ == "__main__":
    asyncio.run(main())