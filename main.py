import asyncio
import logging
import re
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from config.settings import BOT_TOKEN
from bot.services.llm_client import llm_client
from bot.services.database import Database

logging.basicConfig(level=logging.INFO)

# Инициализация
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
db = Database()

def is_poker_related(text: str) -> bool:
    """Проверяет, относится ли текст к покеру"""
    text_lower = text.lower()
    
    # Покерные ключевые слова
    poker_keywords = [
        'покер', 'холдем', 'флоп', 'терн', 'ривер', 'стейк', 'блеф', 
        'колл', 'рейз', 'фолд', 'чек', 'банк', 'дилер', 'раздача',
        'префлоп', 'турнир', 'кэш', 'блайнды', 'позиция', 'рука',
        'комбинация', 'стратегия', 'odds', 'пот', 'ставка', 'аллын',
        'all-in', 'all in', 'банкролл', 'управление', 'психология',
        'карты', 'флеш', 'стрит', 'фулл-хаус', 'сет', 'пара', 'каре',
        'масть', 'чипы', 'фишки', 'стол', 'игрок', 'противник',
        'выиграть', 'проиграть', 'партия', 'мат', 'ожидание', 'шансы',
        'вероятность', 'процент', 'odds', 'пот-оддсы', 'hand', 'range',
        'туз', 'король', 'дама', 'валет', 'десятка', 'девятка'
    ]
    
    # Комбинации карт (AA, KK, AK, 72 и т.д.)
    card_combinations = re.findall(r'\b[akqjt2-9]{2}\b', text_lower)
    
    # Позиции за столом
    positions = ['баттон', 'катофф', 'хиджек', 'мп', 'эп', 'лп', 'бб', 'сб']
    
    return (any(keyword in text_lower for keyword in poker_keywords) or
            any(pos in text_lower for pos in positions) or
            len(card_combinations) > 0 or
            any(word in text_lower for word in ['aa', 'kk', 'qq', 'jj', 'ak', 'aq']))

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    
    # Сохраняем пользователя в БД
    db.save_user(user_id, username, first_name)
    
    await message.answer(
        "🤖 Добро пожаловать в Poker Mentor AI!\n\n"
        "Я ваш персональный покерный тренер с искусственным интеллектом.\n\n"
        "🎯 <b>Доступные команды:</b>\n"
        "/ask [вопрос] - задать вопрос AI\n"
        "/analysis [раздача] - анализ покерной раздачи\n"
        "/stats - ваша статистика\n\n"
        "💡 <b>Просто напишите:</b>\n"
        "• 'AA на префлопе'\n" 
        "• 'Как играть с дро?'\n"
        "• 'Стратегия на баттоне'\n\n"
        "И я помогу вам улучшить игру!",
        parse_mode="HTML"
    )

@dp.message(Command("ask"))
async def ask_handler(message: types.Message):
    """Вопрос к AI"""
    question = message.text.replace('/ask', '').strip()
    
    if not question:
        await message.answer("❌ Напишите вопрос после команды /ask")
        return
    
    user_id = message.from_user.id
    db.increment_ai_requests(user_id)
    
    await message.answer("🤔 Думаю над ответом...")
    
    response = await llm_client.generate_response(question)
    
    # Сохраняем запрос в БД
    db.save_ai_request(user_id, question, response)
    
    await message.answer(f"🎯 <b>Ответ AI:</b>\n\n{response}", parse_mode="HTML")

@dp.message(Command("analysis"))
async def analysis_handler(message: types.Message):
    """Анализ покерной раздачи"""
    hand_text = message.text.replace('/analysis', '').strip()
    
    if not hand_text:
        await message.answer(
            "📝 <b>Опишите раздачу для анализа:</b>\n\n"
            "Примеры:\n"
            "• <i>У меня A♠ K♠ на баттоне, противник рейзит с MP</i>\n"
            "• <i>7♣ 2♦ на BB, оппонент ставит контбет на флопе</i>\n"
            "• <i>JJ в средней позиции, все фолдят до меня</i>",
            parse_mode="HTML"
        )
        return
    
    user_id = message.from_user.id
    db.increment_hand_analysis(user_id)
    
    await message.answer("🔍 Анализирую раздачу...")
    
    prompt = f"""
    Проанализируй эту покерную раздачу как профессиональный тренер:

    {hand_text}

    Дай пошаговый анализ:
    1. Оценка силы руки
    2. Рекомендуемые действия на каждом улице
    3. Математическое обоснование
    4. Долгосрочная ожидаемая ценность (EV)
    5. Рассинг оппонента

    Отвечай кратко и по делу, используя покерную терминологию.
    """
    
    response = await llm_client.generate_response(prompt, 1000)
    
    # Сохраняем запрос в БД
    db.save_ai_request(user_id, f"АНАЛИЗ: {hand_text}", response)
    
    await message.answer(f"📊 <b>Анализ раздачи:</b>\n\n{response}", parse_mode="HTML")

@dp.message(Command("stats"))
async def stats_handler(message: types.Message):
    """Статистика пользователя"""
    user_id = message.from_user.id
    stats = db.get_user_stats(user_id)
    
    await message.answer(
        f"📈 <b>Ваша статистика:</b>\n\n"
        f"• 🤖 Запросов к AI: <b>{stats['ai_requests']}</b>\n"
        f"• 📊 Анализов раздач: <b>{stats['hand_analysis']}</b>\n"
        f"• 📅 Дата регистрации: <b>{stats['registration_date']}</b>",
        parse_mode="HTML"
    )

@dp.message(Command("help"))
async def help_handler(message: types.Message):
    """Помощь по командам"""
    await message.answer(
        "🆘 <b>Помощь по командам:</b>\n\n"
        "/start - начать работу\n"
        "/ask [вопрос] - задать вопрос AI\n"
        "/analysis [раздача] - анализ покерной раздачи\n"
        "/stats - ваша статистика\n"
        "/help - эта справка\n\n"
        "💡 <b>Примеры вопросов:</b>\n"
        "<i>Как играть с парой валетов?</i>\n"
        "<i>Стратегия на флопе с дро</i>\n"
        "<i>Когда делать 3-бет?</i>",
        parse_mode="HTML"
    )

@dp.message()
async def smart_poker_handler(message: types.Message):
    """Умный обработчик всех сообщений"""
    text = message.text.strip()
    
    # Пропускаем команды
    if text.startswith('/'):
        return
    
    # Пропускаем короткие сообщения
    if len(text) < 3:
        return
    
    user_id = message.from_user.id
    
    # Проверяем, относится ли сообщение к покеру
    if is_poker_related(text):
        db.increment_ai_requests(user_id)
        
        await message.answer("🎯 Анализирую вашу ситуацию...")
        
        # Создаем умный промпт в зависимости от содержания
        if any(word in text.lower() for word in ['анализ', 'раздача', 'флоп', 'терн', 'ривер']):
            prompt_type = "анализ раздачи"
            prompt = f"Проанализируй эту покерную ситуацию: {text}"
        elif any(word in text.lower() for word in ['стратегия', 'тактика', 'как играть']):
            prompt_type = "стратегия"
            prompt = f"Дай стратегические рекомендации по этому вопросу: {text}"
        else:
            prompt_type = "общий вопрос"
            prompt = f"Ответь на этот покерный вопрос: {text}"
        
        response = await llm_client.generate_response(prompt)
        
        # Сохраняем запрос в БД
        db.save_ai_request(user_id, f"{prompt_type.upper()}: {text}", response)
        
        await message.answer(f"🤖 <b>Poker Mentor:</b>\n\n{response}", parse_mode="HTML")
    else:
        # Если не покер - вежливо направляем
        await message.answer(
            "🎴 <b>Я специализируюсь на покере!</b>\n\n"
            "Задайте вопрос о:\n"
            "• Покерной стратегии и тактике\n"
            "• Анализе конкретных раздач\n" 
            "• Управлении банкроллом\n"
            "• Психологии покера\n\n"
            "💡 <b>Пример:</b> <i>Как играть с тузом-королем?</i>\n\n"
            "Используйте /analysis для детального разбора раздачи!",
            parse_mode="HTML"
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
        db.close()
        logging.info("👋 Бот остановлен")

if __name__ == "__main__":
    asyncio.run(main())