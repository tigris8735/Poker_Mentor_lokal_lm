import asyncio
import logging
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.services.llm_client import llm_client
from bot.services.database import Database

router = Router()
db = Database()

# Хранилище контекста диалогов (временное)
user_contexts = {}

@router.message(Command("ask"))
async def ask_ai_handler(message: types.Message):
    """Улучшенная команда ask с контекстом"""
    question = message.text.replace('/ask', '').strip()
    
    if not question:
        # Показываем примеры вопросов
        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(
            text="🎯 Примеры вопросов", 
            callback_data="show_examples"
        ))
        
        await message.answer(
            "🤖 <b>AI Помощник по покеру</b>\n\n"
            "Задайте любой вопрос о покере после команды /ask\n\n"
            "<b>Примеры:</b>\n"
            "• <i>Как играть с парой тузов?</i>\n"
            "• <i>Стратегия на баттоне</i>\n"
            "• <i>Когда делать 3-бет?</i>\n"
            "• <i>Как читать оппонентов?</i>",
            reply_markup=builder.as_markup(),
            parse_mode="HTML"
        )
        return
    
    user_id = message.from_user.id
    
    # Получаем контекст предыдущего диалога
    context = user_contexts.get(user_id, "")
    full_prompt = f"{context}\n\nНовый вопрос: {question}" if context else question
    
    await message.answer("🤔 Думаю над ответом...")
    
    try:
        response = await llm_client.generate_response(full_prompt, 1000)
        
        # Сохраняем контекст для продолжения диалога
        user_contexts[user_id] = f"Предыдущий вопрос: {question}\nОтвет: {response}"
        
        # Сохраняем в БД
        db.save_ai_request(user_id, question, response)
        db.increment_ai_requests(user_id)
        
        # Клавиатура для дополнительных действий
        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(
            text="💬 Задать уточняющий вопрос", 
            callback_data="ask_followup"
        ))
        builder.add(types.InlineKeyboardButton(
            text="🎯 Другой вопрос", 
            callback_data="ask_new"
        ))
        
        await message.answer(
            f"🤖 <b>AI Помощник:</b>\n\n{response}",
            reply_markup=builder.as_markup(),
            parse_mode="HTML"
        )
        
    except Exception as e:
        logging.error(f"❌ Ошибка AI запроса: {e}")
        await message.answer("❌ Произошла ошибка при обращении к AI. Попробуйте позже.")

@router.callback_query(lambda c: c.data == "show_examples")
async def show_examples(callback: types.CallbackQuery):
    """Показать примеры вопросов"""
    examples = [
        "🎯 <b>Стратегические вопросы:</b>",
        "• Как играть с парой валетов?",
        "• Когда делать контбет?",
        "• Стратегия на коротком стеке",
        "",
        "📊 <b>Аналитические вопросы:</b>",
        "• Как читать диапазоны оппонентов?",
        "• Когда выгоден блеф?",
        "• Как считать пот-оддсы?",
        "",
        "🧠 <b>Психологические вопросы:</b>",
        "• Как сохранять концентрацию?",
        "• Как справляться с даунстриками?",
        "• Методы чтения оппонентов"
    ]
    
    await callback.message.answer(
        "\n".join(examples) + "\n\nПросто напишите /ask и ваш вопрос!",
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(lambda c: c.data == "ask_followup")
async def ask_followup(callback: types.CallbackQuery):
    """Запрос уточняющего вопроса"""
    await callback.message.answer(
        "💬 Напишите ваш уточняющий вопрос:\n\n"
        "<i>Пример: 'Можешь подробнее объяснить про позиционную игру?'</i>",
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(lambda c: c.data == "ask_new")
async def ask_new_question(callback: types.CallbackQuery):
    """Начать новый вопрос"""
    user_id = callback.from_user.id
    # Очищаем контекст для нового вопроса
    if user_id in user_contexts:
        del user_contexts[user_id]
    
    await callback.message.answer(
        "🎯 Задайте новый вопрос о покере после команды /ask\n\n"
        "<i>Пример: '/ask Как играть с suited connectors?'</i>",
        parse_mode="HTML"
    )
    await callback.answer()

@router.message(Command("clear_context"))
async def clear_context(message: types.Message):
    """Очистка контекста диалога"""
    user_id = message.from_user.id
    if user_id in user_contexts:
        del user_contexts[user_id]
    
    await message.answer("🔄 Контекст диалога очищен. Следующий вопрос будет обработан без учета предыдущих.")

@router.message(Command("ask_advanced"))
async def ask_advanced_handler(message: types.Message):
    """Расширенная версия ask с выбором стиля ответа"""
    question = message.text.replace('/ask_advanced', '').strip()
    
    if not question:
        await message.answer(
            "🎓 <b>Расширенный AI помощник</b>\n\n"
            "Используйте: <code>/ask_advanced [ваш вопрос]</code>\n\n"
            "<b>Особенности:</b>\n"
            "• Более детальные ответы\n"
            "• Математические расчеты\n"
            "• Стратегические рекомендации\n"
            "• Примеры из реальной практики",
            parse_mode="HTML"
        )
        return
    
    await message.answer("🎓 Готовлю расширенный ответ...")
    
    advanced_prompt = f"""
    Вопрос о покере: {question}
    
    Дай развернутый профессиональный ответ включающий:
    1. Подробное объяснение концепции
    2. Математическое обоснование если применимо
    3. Конкретные примеры из игры
    4. Практические рекомендации
    5. Частые ошибки и как их избежать
    
    Будь максимально полезным и конкретным.
    """
    
    response = await llm_client.generate_response(advanced_prompt, 1500)
    
    user_id = message.from_user.id
    db.save_ai_request(user_id, f"РАСШИРЕННЫЙ: {question}", response)
    db.increment_ai_requests(user_id)
    
    await message.answer(
        f"🎓 <b>Расширенный ответ:</b>\n\n{response}",
        parse_mode="HTML"
    )