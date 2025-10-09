from aiogram import Router, types
from aiogram.filters import Command
from bot.services.ai_service import AIService

router = Router()
ai_service = AIService()

@router.message(Command("ai_status"))
async def ai_status_handler(message: types.Message):
    """Показывает статус подключения к AI"""
    
    # Проверяем подключение
    is_connected = await ai_service.check_connection()
    
    if is_connected:
        status_text = "✅ *AI подключен и готов к работе!*\n\nМожете использовать:\n/analyze - анализ раздач\n/advice - советы по игре\n/concept - объяснение концепций"
    else:
        status_text = "❌ *AI временно недоступен*\n\n🤖 Работаем в оффлайн-режиме с базовыми советами.\n\n*Причины:*\n- LM Studio не запущен\n- Проблемы с сетью\n- Модель не загружена\n\n*Рекомендации:*\n1. Проверьте что LM Studio запущен\n2. Убедитесь что модель загружена\n3. Проверьте настройки сети"
    
    await message.answer(status_text, parse_mode="Markdown")

@router.message(Command("debug_ai"))
async def debug_ai_handler(message: types.Message):
    """Тестирует подключение к AI"""
    await message.answer("🔧 Тестируем подключение к AI...")
    
    try:
        # Тестовый запрос
        test_response = await ai_service.get_poker_advice("У меня пара тузов на префлопе")
        await message.answer(f"✅ Тест пройден!\n\nОтвет AI:\n{test_response}")
    except Exception as e:
        await message.answer(f"❌ Ошибка тестирования:\n{str(e)}")