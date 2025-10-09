from aiogram import Router, types
from aiogram.filters import Command
from bot.services.poker_engine import PokerEngine

router = Router()
poker_engine = PokerEngine()

@router.message(Command("game"))
async def game_handler(message: types.Message):
    """Начало новой покерной игры"""
    try:
        # Создаем и перемешиваем колоду
        deck = poker_engine.create_deck()
        deck = poker_engine.shuffle_deck(deck)
        
        # Раздаем карты
        hands, deck = poker_engine.deal_cards(deck, 2)
        
        user_hand = hands[0]
        ai_hand = hands[1]
        
        game_text = f"""
🎮 *Начало игры!*

*Твоя рука:* {poker_engine.format_hand(user_hand)}
*AI рука:* ?? ??

*Ставки:* 10/20
*Твой стек:* 1500

*Действия:*
/fold - Сбросить
/call - Уравнять (20)
/raise - Поднять
        """
        
        await message.answer(game_text, parse_mode="Markdown")
        
    except Exception as e:
        await message.answer(f"❌ Ошибка при начале игры: {e}")