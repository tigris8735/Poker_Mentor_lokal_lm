import asyncio
import logging
from aiogram import Bot
from config.settings import BOT_TOKEN

async def check_bot():
    try:
        bot = Bot(token=BOT_TOKEN)
        bot_info = await bot.get_me()
        print(f"✅ Бот работает: {bot_info.full_name} (@{bot_info.username})")
        await bot.session.close()
        return True
    except Exception as e:
        print(f"❌ Ошибка бота: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(check_bot())