import random
from typing import List, Tuple

class PokerEngine:
    def __init__(self):
        self.suits = ['♥', '♦', '♣', '♠']
        self.ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        
    def create_deck(self) -> List[str]:
        """Создает колоду из 52 карт"""
        deck = []
        for suit in self.suits:
            for rank in self.ranks:
                deck.append(f'{rank}{suit}')
        return deck
    
    def shuffle_deck(self, deck: List[str]) -> List[str]:
        """Перемешивает колоду"""
        random.shuffle(deck)
        return deck
    
    def deal_cards(self, deck: List[str], num_players: int = 2) -> Tuple[List[List[str]], List[str]]:
        """Раздает по 2 карты каждому игроку"""
        hands = [[] for _ in range(num_players)]
        
        # Раздаем по 2 карты каждому игроку
        for card_index in range(2):
            for player_index in range(num_players):
                if deck:
                    card = deck.pop()
                    hands[player_index].append(card)
        
        return hands, deck
    
    def deal_flop(self, deck: List[str]) -> Tuple[List[str], List[str]]:
        """Раздает флоп (3 общие карты)"""
        if deck: 
            deck.pop()  # Сжигаем карту
        flop = [deck.pop() for _ in range(3)] if len(deck) >= 3 else []
        return flop, deck
    
    def deal_turn(self, deck: List[str]) -> Tuple[str, List[str]]:
        """Раздает терн (4-я общая карта)"""
        if deck: 
            deck.pop()  # Сжигаем карту
        turn = deck.pop() if deck else None
        return turn, deck
    
    def deal_river(self, deck: List[str]) -> Tuple[str, List[str]]:
        """Раздает ривер (5-я общая карта)"""
        if deck: 
            deck.pop()  # Сжигаем карту
        river = deck.pop() if deck else None
        return river, deck
    
    def format_hand(self, hand: List[str]) -> str:
        """Форматирует руку для отображения"""
        return ' '.join(hand) if len(hand) == 2 else ' '.join(hand) + ' (неполная рука)'