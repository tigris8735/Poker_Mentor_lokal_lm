from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("fold"))
async def fold_handler(message: types.Message):
    await message.answer("🎴 Вы сбросили карты. Ход переходит к AI.")

@router.message(Command("call"))
async def call_handler(message: types.Message):
    await message.answer("✅ Вы уравняли ставку 20. Ждем ход AI...")

@router.message(Command("raise"))
async def raise_handler(message: types.Message):
    await message.answer("📈 Вы подняли ставку. На сколько поднимаете?")