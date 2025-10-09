from aiogram import Router, types
from aiogram.filters import Command
from bot.services.game_manager import GameManager

router = Router()
game_manager = GameManager()

@router.message(Command("game"))
async def game_handler(message: types.Message):
    """Начало новой игры"""
    user_id = message.from_user.id
    
    game = game_manager.start_game(user_id)
    
    game_text = f"""
🎮 *Начало игры!*

*Ваша рука:* {game.engine.format_hand(game.user_hand)}
*AI рука:* ?? ??

*Ставки:* 10/20 (вы малый блайнд)
*Ваш стек:* {game.user_stack}
*Банк:* {game.pot} 💰

*Действия:*
/fold - Сбросить
/call - Уравнять (20)
/raise - Поднять
    """
    
    await message.answer(game_text, parse_mode="Markdown")

@router.message(Command("fold"))
async def fold_handler(message: types.Message):
    """Игрок сбрасывает карты"""
    user_id = message.from_user.id
    result = game_manager.user_fold(user_id)
    await message.answer(result)

@router.message(Command("call"))
async def call_handler(message: types.Message):
    """Игрок уравнивает ставку"""
    user_id = message.from_user.id
    result = game_manager.user_call(user_id)
    await message.answer(result)

@router.message(Command("raise"))
async def raise_handler(message: types.Message):
    """Игрок поднимает ставку"""
    user_id = message.from_user.id
    result = game_manager.user_raise(user_id)
    await message.answer(result)

@router.message(Command("check"))
async def check_handler(message: types.Message):
    """Игрок чекает (если нет ставки)"""
    user_id = message.from_user.id
    game = game_manager.get_game(user_id)
    
    if not game:
        await message.answer("Нет активной игры. Используйте /game чтобы начать.")
        return
    
    # Проверяем можно ли чекнуть (текущая ставка равна нашей)
    if game.user_contributed == game.current_bet:
        result = game_manager._ai_action(game)  # Ход AI после чека
        await message.answer(f"Вы чекнули.\n{result}")
    else:
        await message.answer("Нельзя чекнуть - есть активная ставка!")