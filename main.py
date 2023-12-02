# This is a simple Python script to play Blackjack
# By Zach Oltman
# Licensed under the MIT License

"""SET-UP"""
from random import shuffle
from itertools import product

RANKS = ("2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A")
FACES = ("J", "Q", "K")
ACE = "A"
SUITS = ("H", "C", "S", "D")
POSSIBLE_NUM_PLAYERS = {"1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6}

"""CLASSES"""


class Deck:
    """A simple representation of a deck of playing cards"""

    def __init__(self, size_multiplier=1):  # creates a deck of multiples of 52 cards and shuffles it
        self.shoe = []
        for r, s in product(RANKS, SUITS):
            self.shoe.append(r + s)
        if size_multiplier != 1:
            dupe = self.shoe
            for i in range(1, size_multiplier-1):
                self.shoe = self.shoe + dupe
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
            if card[0] == ACE:  # aces can be 1 or 11, so the initial value is set for 1...
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

"""FUNCTIONS"""


def play_game(num_players):
    deck = Deck(6)
    shuffle(deck.shoe)
    players = {}
    for player_num in range(0, num_players):  # creates hands for every player, player 0 is the dealer
        players[player_num] = Player(player_num)

    print(f"\nWelcome to this {num_players}-player game of Blackjack!")
    print("Prepping the game...")
    playing = True
    while playing:
        if len(deck.shoe) < 60:
            print("Reshuffling deck...")
            deck = Deck(6)
            shuffle(deck.shoe)


        ok_choice = False
        while not ok_choice:
            keep_playing = input("Play another round? [Y]es or [N]o?")
            if keep_playing.lower() in ("y", "yes"):
                ok_choice = True
            elif keep_playing.lower() in ("n", "no"):
                ok_choice = True
                playing = False
            else:
                print("That wasn't understood, please enter a valid input.")


"""MAIN"""

running = True
while running:
    print("Welcome to Blackjack!")
    valid_choice = False
    while not valid_choice:
        menu_choice = input("How many human players are there? Pick a number between 1 and 6!\n(Enter \"quit\" to exit the game)  ")
        if menu_choice in POSSIBLE_NUM_PLAYERS.keys():
            valid_choice = True
            play_game(POSSIBLE_NUM_PLAYERS[menu_choice])
        elif menu_choice.lower() == "quit":
            valid_choice = True
            running = False
        else:
            print("Sorry, I didn't understand that. Please enter a valid input.")
    print("Thanks for playing!")

"""TEST"""
"""
mydeck = Deck()
print(mydeck.shoe)
print(len(mydeck.shoe))

player1 = Player(1)
mydeck.deal_out(player1)
mydeck.deal_out(player1)
print(player1.get_hand_value())

print(len(mydeck.shoe))
"""
