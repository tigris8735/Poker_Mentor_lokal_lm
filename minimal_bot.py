import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Настройки
BOT_TOKEN = "8359469592:AAFuIN13uE1-clnkjFKdb_yDYoeTg6nxkHg"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("🤖 Бот работает! Используйте /ask для вопросов к AI")

@dp.message(Command("ask"))
async def ask_handler(message: types.Message):
    await message.answer("🤖 AI функция временно отключена для отладки")

async def main():
    logging.info("🚀 Запуск минимального бота...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())