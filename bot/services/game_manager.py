import random
from typing import Dict, List, Optional
from .poker_engine import PokerEngine

class GameState:
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.engine = PokerEngine()
        self.deck = self.engine.create_deck()
        self.engine.shuffle_deck(self.deck)
        
        # Раздаем карты
        hands, self.deck = self.engine.deal_cards(self.deck, 2)
        self.user_hand = hands[0]
        self.ai_hand = hands[1]
        
        # Статус игры
        self.community_cards = []
        self.pot = 0
        self.user_stack = 1500
        self.ai_stack = 1500
        self.current_bet = 20
        self.user_contributed = 10  # Маленький блайнд
        self.ai_contributed = 20    # Большой блайнд
        self.street = "preflop"  # preflop, flop, turn, river
        self.last_action = None
        self.game_active = True

class GameManager:
    def __init__(self):
        self.active_games: Dict[int, GameState] = {}
    
    def start_game(self, user_id: int) -> GameState:
        """Начинает новую игру для пользователя"""
        if user_id in self.active_games:
            del self.active_games[user_id]
        
        game = GameState(user_id)
        game.pot = 30  # Блайнды
        game.user_stack -= 10
        game.ai_stack -= 20
        self.active_games[user_id] = game
        return game
    
    def get_game(self, user_id: int) -> Optional[GameState]:
        """Возвращает активную игру пользователя"""
        return self.active_games.get(user_id)
    
    def end_game(self, user_id: int):
        """Завершает игру пользователя"""
        if user_id in self.active_games:
            del self.active_games[user_id]
    
    def user_fold(self, user_id: int) -> str:
        """Пользователь сбрасывает карты"""
        game = self.get_game(user_id)
        if not game:
            return "Нет активной игры. Используйте /game чтобы начать."
        
        game.game_active = False
        result = "Вы сбросили карты. AI выигрывает банк!"
        self.end_game(user_id)
        return result
    
    def user_call(self, user_id: int) -> str:
        """Пользователь уравнивает ставку"""
        game = self.get_game(user_id)
        if not game:
            return "Нет активной игры. Используйте /game чтобы начать."
        
        call_amount = game.current_bet - game.user_contributed
        if call_amount > game.user_stack:
            return "Недостаточно фишек для уравнивания!"
        
        game.user_stack -= call_amount
        game.user_contributed += call_amount
        game.pot += call_amount
        
        # Ход AI
        return self._ai_action(game)
    
    def user_raise(self, user_id: int, raise_amount: int = 40) -> str:
        """Пользователь поднимает ставку"""
        game = self.get_game(user_id)
        if not game:
            return "Нет активной игры. Используйте /game чтобы начать."
        
        total_needed = (game.current_bet - game.user_contributed) + raise_amount
        if total_needed > game.user_stack:
            return "Недостаточно фишек для поднятия!"
        
        game.user_stack -= total_needed
        game.user_contributed += total_needed
        game.pot += total_needed
        game.current_bet = game.user_contributed
        
        # Ход AI
        return self._ai_action(game)
    
    def _ai_action(self, game: GameState) -> str:
        """Логика хода AI"""
        actions = ["fold", "call", "raise"]
        weights = [0.1, 0.6, 0.3]  # Вероятности действий
        
        action = random.choices(actions, weights)[0]
        
        if action == "fold":
            game.game_active = False
            result = "AI сбросил карты! Вы выиграли банк! 🎉"
            self.end_game(game.user_id)
        
        elif action == "call":
            call_amount = game.current_bet - game.ai_contributed
            if call_amount > game.ai_stack:
                call_amount = game.ai_stack
            
            game.ai_stack -= call_amount
            game.ai_contributed += call_amount
            game.pot += call_amount
            
            # Переход на следующую улицу если оба уравняли
            if game.user_contributed == game.ai_contributed:
                result = self._next_street(game)
            else:
                result = f"AI уравнял ставку. Банк: {game.pot} 💰"
        
        else:  # raise
            raise_amount = random.randint(40, 100)
            total_needed = (game.current_bet - game.ai_contributed) + raise_amount
            
            if total_needed > game.ai_stack:
                total_needed = game.ai_stack
            
            game.ai_stack -= total_needed
            game.ai_contributed += total_needed
            game.pot += total_needed
            game.current_bet = game.ai_contributed
            
            result = f"AI поднял ставку! Текущая ставка: {game.current_bet} 📈"
        
        return result
    
    def _next_street(self, game: GameState) -> str:
        """Переход на следующую улицу"""
        if game.street == "preflop":
            game.street = "flop"
            flop, game.deck = game.engine.deal_flop(game.deck)
            game.community_cards.extend(flop)
            return f"Флоп: {' '.join(flop)}\nБанк: {game.pot} 💰\nВаш ход!"
        
        elif game.street == "flop":
            game.street = "turn"
            turn, game.deck = game.engine.deal_turn(game.deck)
            game.community_cards.append(turn)
            return f"Терн: {turn}\nБанк: {game.pot} 💰\nВаш ход!"
        
        elif game.street == "turn":
            game.street = "river"
            river, game.deck = game.engine.deal_river(game.deck)
            game.community_cards.append(river)
            return f"Ривер: {river}\nБанк: {game.pot} 💰\nВаш ход!"
        
        else:  # river - шоудаун
            return self._showdown(game)
    
    def _showdown(self, game: GameState) -> str:
        """Определение победителя на шоудауне"""
        # Простая логика - случайный победитель
        winner = random.choice(["user", "ai"])
        
        if winner == "user":
            game.user_stack += game.pot
            result = f"🎉 Вы выиграли банк {game.pot}! Ваши карты: {' '.join(game.user_hand)} vs AI: {' '.join(game.ai_hand)}"
        else:
            game.ai_stack += game.pot
            result = f"😞 AI выиграл банк {game.pot}. Ваши карты: {' '.join(game.user_hand)} vs AI: {' '.join(game.ai_hand)}"
        
        self.end_game(game.user_id)
        return result