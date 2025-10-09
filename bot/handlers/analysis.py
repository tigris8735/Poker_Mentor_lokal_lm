from aiogram import Router, types
from aiogram.filters import Command
from bot.services.ai_service import AIService
import logging

router = Router()
ai_service = AIService()
logger = logging.getLogger(__name__)

# Храним состояние ожидания ответа
user_states = {}

@router.message(Command("analyze"))
async def analyze_handler(message: types.Message):
    user_states[message.from_user.id] = "waiting_analysis"
    await message.answer("📝 Опиши раздачу для анализа:\n- Твоя рука\n- Позиция\n- Действия оппонентов\n- Банк")

@router.message(Command("advice"))
async def advice_handler(message: types.Message):
    user_states[message.from_user.id] = "waiting_advice"
    await message.answer("💡 Опиши игровую ситуацию для совета:")

@router.message()
async def handle_user_input(message: types.Message):
    user_id = message.from_user.id
    state = user_states.get(user_id)
    
    if not state:
        return  # Игнорируем сообщения не в состоянии ожидания
    
    try:
        if state == "waiting_analysis":
            await message.answer("🤔 Анализирую раздачу...")
            analysis = await ai_service.analyze_hand(message.text)
            await message.answer(f"🎯 Анализ раздачи:\n\n{analysis}")
            
        elif state == "waiting_advice":
            await message.answer("💭 Обдумываю совет...")
            advice = await ai_service.get_poker_advice(message.text)
            await message.answer(f"📚 Совет:\n\n{advice}")
            
    except Exception as e:
        logger.error(f"AI error: {e}")
        await message.answer("❌ Ошибка при обращении к AI. Проверьте подключение к LM Studio.")
    
    # Сбрасываем состояние
    user_states.pop(user_id, None)