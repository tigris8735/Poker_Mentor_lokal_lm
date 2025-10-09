import asyncio
import random
import logging
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.services.llm_client import llm_client

router = Router()

# Хранилище активных игр
active_games = {}

class PokerGame:
    def __init__(self, user_id):
        self.user_id = user_id
        self.user_hand = []
        self.ai_hand = []
        self.user_chips = 1000
        self.ai_chips = 1000
        self.pot = 0
        self.user_bet = 0
        self.ai_bet = 0
        self.deck = []
        self.stage = "preflop"  # preflop, flop, turn, river
        self.community_cards = []
        self.game_over = False
        
    def init_deck(self):
        """Инициализация колоды"""
        suits = ['♠', '♥', '♦', '♣']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.deck = [f'{rank}{suit}' for suit in suits for rank in ranks]
        random.shuffle(self.deck)
    
    def deal_cards(self):
        """Раздача карт"""
        self.user_hand = [self.deck.pop(), self.deck.pop()]
        self.ai_hand = [self.deck.pop(), self.deck.pop()]
    
    def deal_community_cards(self):
        """Раздача общих карт"""
        if self.stage == "flop":
            self.community_cards = [self.deck.pop() for _ in range(3)]
        elif self.stage in ["turn", "river"]:
            self.community_cards.append(self.deck.pop())
    
    def get_game_state(self, show_ai_cards=False):
        """Получение состояния игры"""
        user_hand_str = " ".join(self.user_hand)
        ai_hand_str = " ".join(self.ai_hand) if show_ai_cards else "❓ ❓"
        community_str = " ".join(self.community_cards) if self.community_cards else "Карты еще не сданы"
        
        return f"""
🎮 <b>Покер 1x1 vs AI</b>

<b>Ваши фишки:</b> {self.user_chips} 🟡
<b>Фишки AI:</b> {self.ai_chips} 🟡  
<b>Банк:</b> {self.pot} 🟡

<b>Ваша рука:</b> {user_hand_str}
<b>Рука AI:</b> {ai_hand_str}

<b>Общие карты ({self.stage}):</b> {community_str}

<b>Ваша ставка:</b> {self.user_bet}
<b>Ставка AI:</b> {self.ai_bet}
        """.strip()
    
    def get_actions_keyboard(self):
        """Клавиатура с доступными действиями"""
        builder = InlineKeyboardBuilder()
        
        if self.user_bet == self.ai_bet:
            builder.add(types.InlineKeyboardButton(text="📥 Чек", callback_data="action_check"))
            builder.add(types.InlineKeyboardButton(text="💰 Ставка", callback_data="action_bet"))
        else:
            builder.add(types.InlineKeyboardButton(text="📞 Колл", callback_data="action_call"))
            builder.add(types.InlineKeyboardButton(text="📈 Рейз", callback_data="action_raise"))
        
        builder.add(types.InlineKeyboardButton(text="📤 Фолд", callback_data="action_fold"))
        builder.add(types.InlineKeyboardButton(text="🔍 Анализ руки", callback_data="action_analysis"))
        
        builder.adjust(2)
        return builder.as_markup()
    
    async def ai_decision(self):
        """Решение AI о ходе"""
        game_context = f"""
Игра в покер. Стадия: {self.stage}
Общие карты: {', '.join(self.community_cards)}
Моя рука (AI): {', '.join(self.ai_hand)}
Ставка игрока: {self.user_bet}
Моя текущая ставка: {self.ai_bet}
Банк: {self.pot}
Мои фишки: {self.ai_chips}
Фишки игрока: {self.user_chips}

Какое действие следует сделать? Ответь одним словом: CHECK, CALL, RAISE или FOLD. Объясни кратко почему.
        """.strip()
        
        try:
            response = await llm_client.generate_response(game_context, 200)
            logging.info(f"🤖 AI решение: {response}")
            
            # Простой парсинг ответа AI
            response_lower = response.lower()
            if "фолд" in response_lower or "fold" in response_lower:
                return "fold"
            elif "рейз" in response_lower or "raise" in response_lower:
                return "raise"
            elif "колл" in response_lower or "call" in response_lower:
                return "call"
            else:
                return "check"
                
        except Exception as e:
            logging.error(f"❌ Ошибка AI решения: {e}")
            # Фолбэк: случайное решение
            return random.choice(["check", "call", "fold"])

@router.message(Command("poker"))
async def start_poker_game(message: types.Message):
    """Начало новой покерной игры"""
    user_id = message.from_user.id
    
    if user_id in active_games:
        await message.answer("🎮 У вас уже есть активная игра! Используйте /end_game чтобы завершить её.")
        return
    
    # Создаем новую игру
    game = PokerGame(user_id)
    game.init_deck()
    game.deal_cards()
    active_games[user_id] = game
    
    await message.answer(
        game.get_game_state(),
        reply_markup=game.get_actions_keyboard(),
        parse_mode="HTML"
    )

@router.callback_query(lambda c: c.data.startswith("action_"))
async def handle_game_action(callback: types.CallbackQuery):
    """Обработка действий в игре"""
    user_id = callback.from_user.id
    
    if user_id not in active_games:
        await callback.message.edit_text("❌ Игра не найдена. Начните новую игру /poker")
        return
    
    game = active_games[user_id]
    action = callback.data.replace("action_", "")
    
    if action == "analysis":
        # Анализ текущей руки AI
        await analyze_current_hand(callback, game)
        return
    
    if action == "check":
        game.user_bet = game.ai_bet
    elif action == "call":
        call_amount = game.ai_bet - game.user_bet
        if game.user_chips >= call_amount:
            game.user_chips -= call_amount
            game.user_bet = game.ai_bet
            game.pot += call_amount
    elif action == "bet":
        bet_amount = 100  # Фиксированная ставка
        if game.user_chips >= bet_amount:
            game.user_chips -= bet_amount
            game.user_bet += bet_amount
            game.pot += bet_amount
    elif action == "raise":
        raise_amount = 200  # Фиксированный рейз
        if game.user_chips >= raise_amount:
            game.user_chips -= raise_amount
            game.user_bet += raise_amount
            game.pot += raise_amount
    elif action == "fold":
        await callback.message.edit_text(
            "📤 Вы сбросили карты. AI побеждает!\n\n"
            f"Карты AI: {' '.join(game.ai_hand)}\n"
            f"Используйте /poker для новой игры.",
            parse_mode="HTML"
        )
        del active_games[user_id]
        return
    
    # Ход AI
    await callback.message.edit_text(f"🎮 Ваш ход принят... AI думает...")
    ai_action = await game.ai_decision()
    
    # Обработка хода AI
    if ai_action == "fold":
        await callback.message.edit_text(
            "🎉 AI сбросил карты! Вы победили!\n\n"
            f"Ваш выигрыш: {game.pot} фишек\n"
            f"Используйте /poker для новой игры.",
            parse_mode="HTML"
        )
        del active_games[user_id]
        return
    elif ai_action == "call":
        call_amount = game.user_bet - game.ai_bet
        if game.ai_chips >= call_amount:
            game.ai_chips -= call_amount
            game.ai_bet = game.user_bet
            game.pot += call_amount
    elif ai_action == "raise":
        raise_amount = 200
        if game.ai_chips >= raise_amount:
            game.ai_chips -= raise_amount
            game.ai_bet += raise_amount
            game.pot += raise_amount
    
    # Переход к следующей стадии если ставки равны
    if game.user_bet == game.ai_bet:
        stages = ["preflop", "flop", "turn", "river", "showdown"]
        current_index = stages.index(game.stage)
        if current_index < len(stages) - 1:
            game.stage = stages[current_index + 1]
            if game.stage != "showdown":
                game.deal_community_cards()
    
    # Проверка окончания игры
    if game.stage == "showdown" or game.user_chips <= 0 or game.ai_chips <= 0:
        await show_game_result(callback.message, game, user_id)
        return
    
    # Обновление состояния игры
    await callback.message.edit_text(
        game.get_game_state(),
        reply_markup=game.get_actions_keyboard(),
        parse_mode="HTML"
    )

async def analyze_current_hand(callback: types.CallbackQuery, game: PokerGame):
    """Анализ текущей руки AI"""
    analysis_prompt = f"""
Проанализируй покерную руку и ситуацию:

Рука игрока: {', '.join(game.user_hand)}
Общие карты: {', '.join(game.community_cards)}
Стадия: {game.stage}

Дай краткий анализ:
1. Сила руки на текущий момент
2. Рекомендации по игре
3. Потенциальные комбинации
    """
    
    await callback.answer("🔍 Анализирую вашу руку...")
    
    analysis = await llm_client.generate_response(analysis_prompt, 300)
    
    await callback.message.answer(
        f"📊 <b>Анализ вашей руки:</b>\n\n{analysis}",
        parse_mode="HTML"
    )

async def show_game_result(message: types.Message, game: PokerGame, user_id: int):
    """Показать результат игры"""
    # Простое определение победителя по силе руки
    user_strength = evaluate_hand_strength(game.user_hand + game.community_cards)
    ai_strength = evaluate_hand_strength(game.ai_hand + game.community_cards)
    
    if user_strength > ai_strength:
        result_text = "🎉 Вы победили!"
        game.user_chips += game.pot
    elif ai_strength > user_strength:
        result_text = "🤖 AI победил!"
        game.ai_chips += game.pot
    else:
        result_text = "🤝 Ничья!"
        game.user_chips += game.pot // 2
        game.ai_chips += game.pot // 2
    
    await message.answer(
        f"{result_text}\n\n"
        f"<b>Ваша рука:</b> {' '.join(game.user_hand)}\n"
        f"<b>Рука AI:</b> {' '.join(game.ai_hand)}\n"
        f"<b>Общие карты:</b> {' '.join(game.community_cards)}\n\n"
        f"<b>Ваш баланс:</b> {game.user_chips} фишек\n"
        f"<b>Баланс AI:</b> {game.ai_chips} фишек\n\n"
        f"Используйте /poker для новой игры!",
        parse_mode="HTML"
    )
    
    del active_games[user_id]

def evaluate_hand_strength(cards):
    """Упрощенная оценка силы руки (для демо)"""
    # В реальной игре нужно реализовать полноценную оценку покерных рук
    return random.randint(1, 100)

@router.message(Command("end_game"))
async def end_current_game(message: types.Message):
    """Завершение текущей игры"""
    user_id = message.from_user.id
    
    if user_id in active_games:
        del active_games[user_id]
        await message.answer("🎮 Игра завершена. Используйте /poker для новой игры!")
    else:
        await message.answer("❌ У вас нет активных игр.")

@router.message(Command("game_stats"))
async def show_game_stats(message: types.Message):
    """Показать статистику игр"""
    user_id = message.from_user.id
    active_count = len(active_games)
    
    await message.answer(
        f"📊 <b>Статистика игр:</b>\n\n"
        f"• Активных игр: {active_count}\n"
        f"• Ваша активная игра: {'✅' if user_id in active_games else '❌'}\n\n"
        f"Используйте /poker для начала игры!",
        parse_mode="HTML"
    )