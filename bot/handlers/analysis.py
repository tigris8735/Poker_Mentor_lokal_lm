from aiogram import Router, types
from aiogram.filters import Command
from bot.services.ai_service import AIService

router = Router()
ai_service = AIService()

@router.message(Command("analyze"))
async def analyze_handler(message: types.Message):
    await message.answer("📝 Опиши раздачу для анализа:\n- Твоя рука\n- Позиция\n- Действия оппонентов\n- Банк")

@router.message(Command("advice"))
async def advice_handler(message: types.Message):
    await message.answer("💡 Опиши игровую ситуацию для совета:")

@router.message(lambda message: message.reply_to_message and 
                message.reply_to_message.text in ["📝 Опиши раздачу для анализа:", "💡 Опиши игровую ситуацию для совета:"])
async def process_analysis(message: types.Message):
    await message.answer("🤔 Анализирую...")
    
    if "раздачу" in message.reply_to_message.text:
        analysis = await ai_service.analyze_hand(message.text)
    else:
        analysis = await ai_service.get_poker_advice(message.text)
    
    await message.answer(f"🎯 Анализ:\n\n{analysis}")