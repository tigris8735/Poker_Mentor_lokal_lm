from aiogram import Router, types
from aiogram.filters import Command
from bot.services.poker_engine import PokerEngine
from bot.services.ai_service import AIService

router = Router()
poker_engine = PokerEngine()
ai_service = AIService()

@router.message(Command("game"))
async def game_handler(message: types.Message):
    # Начало новой игры
    deck = poker_engine.create_deck()
    deck = poker_engine.shuffle_deck(deck)
    hands, deck = poker_engine.deal_cards(deck)
    
    user_hand = hands[0]
    ai_hand = hands[1]
    
    game_text = f"""
    🎮 Начало игры!
    
    Твоя рука: {' '.join(user_hand)}
    AI рука: ?? ??
    
    Ставки: 10/20
    Твой стек: 1500
    
    Действия:
    /fold - Сбросить
    /call - Уравнять (20)
    /raise - Поднять
    """
    
    await message.answer(game_text)