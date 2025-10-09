from aiogram import Router, types
from aiogram.filters import Command
from bot.services.game_manager import GameManager

router = Router()
game_manager = GameManager()

@router.message(Command("status"))
async def game_status_handler(message: types.Message):
    """Показывает текущее состояние игры"""
    user_id = message.from_user.id
    game = game_manager.get_game(user_id)
    
    if not game:
        await message.answer("❌ Нет активной игры. Используйте /game чтобы начать.")
        return
    
    status_text = f"""
📊 *Текущая игра*

*Улица:* {game.street}
*Ваша рука:* {game.engine.format_hand(game.user_hand)}
*Общие карты:* {' '.join(game.community_cards) if game.community_cards else 'Нет'}
*Ваш стек:* {game.user_stack} 💰
*Стек AI:* {game.ai_stack} 💰
*Банк:* {game.pot} 💰
*Текущая ставка:* {game.current_bet}

*Доступные действия:*
/fold - Сбросить
/call - Уравнять
/raise - Поднять
/check - Чек (если нет ставки)
    """
    
    await message.answer(status_text, parse_mode="Markdown")

@router.message(Command("end"))
async def end_game_handler(message: types.Message):
    """Завершает текущую игру"""
    user_id = message.from_user.id
    game_manager.end_game(user_id)
    await message.answer("🎯 Игра завершена. Используйте /game для новой игры.")