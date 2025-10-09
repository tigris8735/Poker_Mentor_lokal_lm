from aiogram import Router, types
from aiogram.filters import Command
from bot.services.ai_service import ai_service
from bot.services.database import Database

router = Router()
db = Database()

@router.message(Command("analysis"))
async def analysis_handler(message: types.Message):
    hand_text = message.text.replace('/analysis', '').strip()
    
    if not hand_text:
        await message.answer(
            "📝 <b>Анализ покерной раздачи</b>\n\n"
            "Опишите раздачу после команды /analysis\n\n"
            "<b>Примеры:</b>\n"
            "• <i>У меня A♠ K♠ на баттоне, противник рейзит с MP</i>\n"
            "• <i>7♣ 2♦ на BB, оппонент ставит контбет на флопе J♥8♦3♣</i>\n"
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
    
    response = await ai_service.get_ai_response(prompt)
    
    db.save_ai_request(user_id, f"АНАЛИЗ: {hand_text}", response)
    
    await message.answer(f"📊 <b>Анализ раздачи:</b>\n\n{response}", parse_mode="HTML")