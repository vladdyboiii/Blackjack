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

# these are options while players are navigating menus, they have to be lowercase b/c of the get_player_input function
YES = ("y", "yes")
NO = ("n", "no")
QUIT = ("q", "quit")
HIT = ("h", "hit")
STAND = ("s", "stand")
LOOK = ("l", "look")

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

    def display_hands(self, dealer_hidden=False):    # returns info about the player's hand in a legible manner
        legible_hand = ""
        legible_values = ""
        hand_size = len(self.hand)
        hand_values = self.get_hand_value()
        num_hand_values = len(hand_values)

        if dealer_hidden and self.player_number == 0:   # the dealer's second card is hidden until after all players have made their turn
            display = f"The Dealer has {self.hand[0]} and one face-down card."

        else:   # for all other cases, the hand's legible value is gotten below:
            if self.player_number == 0:    # this if/else gets the player number or if 0, recognizes them as the dealer
                player = "The Dealer"
            else:
                player = f"Player {self.player_number}"

            if hand_size == 2:  # prints the cards legibly depending on if there is two or more cards
                legible_hand = self.hand[0] + " and " + self.hand[1]
            else:
                for i in range(0, hand_size-2):
                    legible_hand = legible_hand + self.hand[i] + ", "
                legible_hand = legible_hand + "and " + self.hand[-1]

            if num_hand_values == 1:    # prints the hand value(s) legibly depending on if there are 1, 2, or more possible values (depending on aces)
                display = player + " has " + legible_hand + ". Their hand's value is " + str(hand_values[0]) + "."
            elif num_hand_values == 2:
                display = player + " has " + legible_hand + ". Their hand's value could be " + str(hand_values[0]) + " or " + str(hand_values[1]) + "."
            else:
                for i in range(0, num_hand_values-1):
                    legible_values = legible_values + hand_values[i] + ", "
                display = player + " has " + legible_hand + ". Their hand's value could be " + legible_values + "or " + str(hand_values[-1]) + "."

        return display  # returns the string to display

    def player_turn(self, deck, players):  # the goings-on of a player's turn
        print(f"It's Player {self.player_number}'s turn!")

        busted = False
        standing = False
        while not busted or standing:
            print(self.display_hands())
            choice = get_player_choice("Would you like to [H]it, [S]tand, or [L]ook around the table at everyone else's hands", (HIT, STAND, LOOK))

            if choice in LOOK:
                for i in players:
                    if i == 0:
                        print(players[i].display_hands(dealer_hidden=True))
                    else:
                        print(players[i].display_hands())

            elif choice in HIT:
                deck.deal_out(self)
                print(f"You just got dealt a {self.hand[-1]}.")
                if all(hv > 21 for hv in self.get_hand_value()):
                    busted = True
                    print(self.display_hands())
                    print(f"Player {self.player_number} has busted!")

            elif choice in STAND:
                standing = True
                print(f"Player {self.player_number} has chosen to stand at {max(hv < 22 for hv in self.get_hand_value())}!")

        if busted:
            return -1
        elif standing:
            return max(hv < 22 for hv in self.get_hand_value())

    def dealer_turn(self, deck):
        print("It's The Dealer's turn! The Dealer will hit until they reach at least 17")
        print("Revealing their hand...")

        busted = False
        standing = False
        while not busted or standing:
            print(print(self.display_hands()))
            if max(hv < 22 for hv in self.get_hand_value()) >= 17:  # checks if dealer's hand has reached 17
                standing = True
                print(f"The Dealer must stand at {max(hv < 22 for hv in self.get_hand_value())}")
            elif all(hv > 21 for hv in self.get_hand_value()):  # checks if dealer has busted
                busted = True
                print("The Dealer has busted!")
            else:
                deck.deal_out(self)
                print(f"The dealer must hit, and has drawn a {self.hand[-1]}.")

        if busted:
            return -1
        elif standing:
            return max(hv < 22 for hv in self.get_hand_value())

    def check_for_blackjack(self):  # checks to see if a player or the dealer has been dealt a natural blackjack
        first_card = self.hand[0]
        second_card = self.hand[1]
        if (first_card[0] in (FACES, "10") and second_card[0] == ACE) or (first_card[0] == ACE and second_card[0] in (FACES, "10")):
            return True
        else:
            return False


"""FUNCTIONS"""


def get_player_choice(question, valid_inputs):
    """A function that gets a player's choice using menu options, re-asking if the input is not understood"""

    player_input = input(question).lower()
    valid_choice = False
    while not valid_choice:
        if any(player_input in vi for vi in valid_inputs):
            valid_choice = True
        else:
            print("That wasn't understood, please enter a valid input.")
            player_input = input(question)
    return player_input


def play_game(num_players):
    """A function that plays a #-player game of Blackjack"""

    deck = Deck(6)
    shuffle(deck.shoe)
    players = {}

    print(f"\nWelcome to this {num_players}-player game of Blackjack!")
    print("Prepping the game...")
    playing = True

    while playing:
        results = {}

        if len(deck.shoe) < 60:
            print("Reshuffling deck...")
            deck = Deck(6)
            shuffle(deck.shoe)

        for player_num in range(0, num_players):  # creates new hands for every player, player 0 is the dealer
            players[player_num] = Player(player_num)
            deck.deal_out(players[player_num])
            deck.deal_out(players[player_num])
            print(players[player_num].display_hands(dealer_hidden=True))

            if players[player_num].check_for_blackjack():   # checks to see if anyone has a natural blackjack, which is an auto-win
                results[player_num] = "Blackjack"
                if player_num == 0:
                    print(players[player_num].display_hands(dealer_hidden=False))
                    print("The Dealer has been dealt a natural Blackjack!")
                else:
                    print(f"Player {player_num} has been dealt a natural Blackjack!")
        print()

        if results[0] == "Blackjack":   # if the dealer has a blackjack, the game is over automatically
            print("Since The Dealer has a natural Blackjack, the game is automatically over!")
            for player_num in results:
                print(f"Player {player_num} also has a natural Blackjack, and thus doesn't lose.")
            for player_num in range(1, num_players):
                if player_num not in results:
                    print(f"Player {player_num} loses with a {max(hv < 22 for hv in players[player_num].get_hand_value())}.")

        else:
            for player_num in range(1, num_players):   # each player's turn
                if results[player_num] == "Blackjack":
                    print(f"Player {player_num}'s turn is skipped as they were dealt a natural Blackjack.")
                else:
                    results[player_num] = players[player_num].player_turn(deck, players.values())
                print()

            results[0] = players[0].dealer_turn(deck)   # dealer's turn
            print()

            print("The round is over!")
            if results[0] == -1:
                print("The Dealer busted this round!")
            else:
                print(f"The Dealer has a {results[0]}.")

            for player_num in range(1, num_players):
                if results[player_num] == -1:
                    print(f"Player {player_num} busted, and thus loses this round.")
                elif results[player_num] > results[0]:
                    print(f"Player {player_num} beats The Dealer with a {results[player_num]}!")
                else:
                    print(f"Player {player_num} loses with a {results[player_num]}.")

        keep_playing = get_player_choice("Play another round?   ", [YES, NO])
        if keep_playing in NO:
            playing = False
            print("Quitting back to the main menu...")
        elif keep_playing in YES:
            playing = True
            print("Another round it is!")


"""MAIN"""

running = True
while running:
    print("Welcome to Blackjack!")
    menu_choice = get_player_choice("How many human players are there? Pick a number between 1 and 6!\n(Enter \"[Q]uit\" to exit the game)    ", (POSSIBLE_NUM_PLAYERS, QUIT))
    if menu_choice in POSSIBLE_NUM_PLAYERS.keys():
        play_game(POSSIBLE_NUM_PLAYERS[menu_choice])
    elif menu_choice in QUIT:
        running = False
        print("Thanks for playing!")
