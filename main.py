import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram import types
from config.settings import BOT_TOKEN
from bot.services.llm_client import llm_client
from bot.services.database import Database

logging.basicConfig(level=logging.INFO)

# Инициализация
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
db = Database()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name
    
    # Сохраняем пользователя в БД
    db.save_user(user_id, username)
    
    await message.answer(
        "🤖 Добро пожаловать в Poker Mentor AI!\n\n"
        "Я ваш персональный покерный тренер с искусственным интеллектом.\n\n"
        "🔹 Задавайте вопросы о покерной стратегии\n"
        "🔹 Анализируйте раздачи командой /analysis\n"
        "🔹 Получайте персональные советы\n\n"
        "Пример: 'Какая стратегия на префлопе с парой десятков?'"
    )

@dp.message(Command("analysis"))
async def analysis_handler(message: types.Message):
    hand_text = message.text.replace('/analysis', '').strip()
    
    if not hand_text:
        await message.answer("📝 Опишите раздачу для анализа:\n\nПример: 'У меня A♠ K♠ на баттоне, противник рейзит с MP'")
        return
    
    await message.answer("🔍 Анализирую раздачу...")
    
    prompt = f"""
    Проанализируй эту покерную раздачу как профессиональный тренер:
    
    {hand_text}
    
    Дай пошаговый анализ:
    1. Сила руки на каждом этапе
    2. Рекомендуемые действия
    3. Математическое обоснование
    4. Долгосрочная ожидаемая ценность
    """
    
    response = await llm_client.generate_response(prompt, 800)
    await message.answer(f"📊 Анализ раздачи:\n\n{response}")

@dp.message(Command("stats"))
async def stats_handler(message: types.Message):
    user_id = message.from_user.id
    stats = db.get_user_stats(user_id)
    
    await message.answer(
        f"📈 Ваша статистика:\n"
        f"• Запросов к AI: {stats['ai_requests']}\n"
        f"• Анализов раздач: {stats['hand_analysis']}\n"
        f"• Дата регистрации: {stats['registration_date']}"
    )

@dp.message()
async def poker_advisor(message: types.Message):
    text = message.text.strip().lower()
    
    # Покерные ключевые слова
    poker_terms = [
        'покер', 'холдем', 'флоп', 'терн', 'ривер', 'стейк', 'блеф', 
        'колл', 'рейз', 'фолд', 'чек', 'банк', 'дилер', 'раздача',
        'префлоп', 'турнир', 'кэш', 'блайнды', 'позиция', 'рука',
        'комбинация', 'стратегия', 'odds', 'пот', 'ставка', 'аллын'
    ]
    
    is_poker_question = any(term in text for term in poker_terms)
    
    if len(text) > 8 and is_poker_question:
        user_id = message.from_user.id
        db.increment_ai_requests(user_id)
        
        await message.answer("🤔 Анализирую вопрос...")
        response = await llm_client.generate_response(text)
        await message.answer(f"🎯 Профессиональный совет:\n\n{response}")
    elif len(text) > 5:
        await message.answer(
            "🎴 Я специализируюсь на покере. Задайте вопрос о:\n"
            "• Стратегии и тактике\n• Анализе конкретных раздач\n" 
            "• Управлении банкроллом\n• Психологии покера\n\n"
            "Используйте /analysis для детального разбора раздачи!"
        )

async def main():
    # Инициализация БД
    db.init_db()
    
    # Проверка бота
    bot_info = await bot.get_me()
    logging.info(f"✅ Бот запущен: {bot_info.full_name}")
    
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"❌ Ошибка: {e}")
    finally:
        await llm_client.close()
        logging.info("👋 Бот остановлен")

if __name__ == "__main__":
    asyncio.run(main())