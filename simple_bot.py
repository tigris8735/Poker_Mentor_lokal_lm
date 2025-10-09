import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from config.settings import BOT_TOKEN
from bot.services.llm_client import llm_client

logging.basicConfig(level=logging.INFO)

# Создаем бота и диспетчер
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()



@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("🤖 Бот работает! Задайте вопрос о покере.")

@dp.message(Command("ask"))
async def ask_handler(message: types.Message):
    question = message.text.replace('/ask', '').strip()
    if not question:
        await message.answer("Напишите вопрос после команды /ask")
        return
    
    await message.answer("🤔 Думаю...")
    response = await llm_client.generate_response(question)
    await message.answer(f"🤖 Ответ:\n\n{response}")

@dp.message()
async def any_message_handler(message: types.Message):
    text = message.text.strip()
    if len(text) > 10:  # Отвечаем на длинные сообщения
        await message.answer("💭 Анализирую...")
        response = await llm_client.generate_response(text)
        await message.answer(f"🎯 Совет:\n\n{response}")

async def main():
    logging.info("🚀 Запуск упрощенного бота...")
    try:
        # Проверяем бота
        bot_info = await bot.get_me()
        logging.info(f"✅ Бот: {bot_info.full_name}")
        
        # Запускаем поллинг
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"❌ Ошибка: {e}")
    finally:
        await llm_client.close()

@dp.message()
async def any_message_handler(message: types.Message):
    text = message.text.strip().lower()
    
    # Список покерных ключевых слов
    poker_keywords = [
        'покер', 'холдем', 'флоп', 'терн', 'ривер', 'стейк', 'блеф', 
        'колл', 'рейз', 'фолд', 'чек', 'банкролл', 'дилер', 'раздача',
        'префлоп', 'постфлоп', 'турнир', 'кэш', 'блайнды', 'позиция',
        'карты', 'рука', 'комбинация', 'стратегия', 'тактика', 'odds',
        'пот', 'ставка', 'аллын', 'чекрейз', 'контбет', 'спекулятивный'
    ]
    
    # Проверяем, содержит ли сообщение покерные термины
    is_poker_related = any(keyword in text for keyword in poker_keywords)
    
    if len(text) > 5 and is_poker_related:
        await message.answer("💭 Анализирую покерную ситуацию...")
        response = await llm_client.generate_response(text)
        await message.answer(f"🎯 Профессиональный совет:\n\n{response}")
    elif len(text) > 10:
        await message.answer("🤖 Я специализируюсь на покере. Задайте вопрос о покерной стратегии, раздачах или тактике!")

if __name__ == "__main__":
    asyncio.run(main())