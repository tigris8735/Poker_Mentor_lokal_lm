from aiogram import Router, types

router = Router()

@router.message()
async def fallback_handler(message: types.Message):
    """Обработчик для любых сообщений без конкретного обработчика"""
    if message.text:
        await message.answer("Используйте команды из меню или напишите /start для помощи")