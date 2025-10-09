import random
from typing import List, Dict

class PokerEngine:
    def __init__(self):
        self.suits = ['♥', '♦', '♣', '♠']
        self.ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        
    def create_deck(self):
        return [f'{rank}{suit}' for suit in self.suits for rank in self.ranks]
    
    def shuffle_deck(self, deck):
        random.shuffle(deck)
        return deck
    
    def deal_cards(self, deck, num_players=2):
        hands = [[] for _ in range(num_players)]
        for _ in range(2):
            for i in range(num_players):
                if deck:
                    hands[i].append(deck.pop())
        return hands, deck
    
    def deal_flop(self, deck):
        if deck: deck.pop()  # burn card
        flop = [deck.pop() for _ in range(3)] if len(deck) >= 3 else []
        return flop, deck
    
    def deal_turn(self, deck):
        if deck: deck.pop()  # burn card
        turn = deck.pop() if deck else None
        return turn, deck
    
    def deal_river(self, deck):
        if deck: deck.pop()  # burn card
        river = deck.pop() if deck else None
        return river, deck