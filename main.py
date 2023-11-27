# This is a simple Python script to play Blackjack
# By Zach Oltman
# Licensed under the MIT License

from random import shuffle
from itertools import product

RANKS = ("2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A")
FACES = ("J", "Q", "K")
SUITS = ("H", "C", "S", "D")


class Deck:
    """A simple representation of a deck of playing cards"""

    def __init__(self):  # creates a deck of 52 cards and shuffles it
        self.shoe = []
        for r, s in product(RANKS, SUITS):
            self.shoe.append(r + s)
        shuffle(self.shoe)

    def deal_out(self, player):  # deals a card out from the deck
        top_card = self.shoe.pop(0)
        player.hand.append(top_card)


class Player:
    """A simple representation of a player and their hand"""

    def __init__(self, player_number):
        self.player_number = player_number
        self.hand = []

    def get_hand_value(self):  # returns the value(s) of a player's hand
        hand_values = [0]
        num_aces = 0

        for card in self.hand:  # adds each card's value to a variable
            if card[0] == "A":  # aces can be 1 or 11, so the initial value is set for 1...
                hand_values[0] += 1
                num_aces += 1
            elif card[0] in FACES:  # face cards are worth 10
                hand_values[0] += 10
            else:  # number cards are worth their value
                hand_values[0] += int(card[0])

        for i in range(num_aces):  # ... and new hand values are created by adding 10! (1 or 11)
            hand_values.append(hand_values[i - 1] + 10)

        return hand_values


# class Dealer:


"""MAIN"""
mydeck = Deck()
print(mydeck.shoe)
print(len(mydeck.shoe))

player1 = Player(1)
mydeck.deal_out(player1)
mydeck.deal_out(player1)
print(player1.get_hand_value())

print(len(mydeck.shoe))
