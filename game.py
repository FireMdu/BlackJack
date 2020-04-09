"""This script is a allows a single player to play a game of BlackJack
against a computer:

The rules have been dumbed down for ease of coding the game: More
functionality to be added in the future.
"""
import pdb
from numpy import arange, array, concatenate
from itertools import product
from random import shuffle
from knapsack import knapsack
from sys import platform
from os import system
from texttable import Texttable


def clear_screen():
    """Clear command window screen"""

    if platform == "linux" or platform == "linux2" or platform == "darwin":
        system('clear')
    elif platform == "win32":
        system('cls')


class Chip:
    """Class holds objects attributes of each chip denomination a player has.

        The following parameters are mandatory for creating a class instance.

        -`denomination` - Denomination number of the chip, defaults to 1
        -`balance` - Balance of the specified denomination, defaults to 0
        to 0
        """
    DENOMINATIONS = [1, 2, 5, 10, 20, 25, 50, 100, 250, 500, 1000, 2000, 5000]

    def __init__(self, balance_list=None):
        # current chips owned
        if balance_list is None:
            balance_list = []
        self.chips = balance_list
        self.frequency_dict = {}

    @property
    def get_frequency_dict(self):
        return {num: self.chips.count(num) for num in self.chips}

    @staticmethod
    def get_chip_knapsack(amount, choices, recursive=True):
        obtained_chips = []
        done = False
        while not done:
            # get possible candidate denominations
            values = [pick for pick in sorted(choices) if pick <= amount]
            if len(values) > 7 and amount < sorted(choices)[-2]:
                values.pop()
            # [1] * len(values) = weight of each denomination in values list
            _, results_list = knapsack(values, [1]*len(values)).solve(amount)
            results = [values[num] for num in results_list]
            if amount:
                obtained_chips.extend(results)
                amount -= sum(results)
                if not recursive:
                    done = True
            else:
                done = True
        return obtained_chips

    def pull_from_knapsack(self, amount):
        while amount:
            pick_list = [key for key, _ in self.get_frequency_dict.items()
                         if key <= amount]
            # if amount less than 4th last term from Denominations then use
            # the knapsack technique to pick from list
            if amount < self.DENOMINATIONS[-4]:
                pick = self.get_chip_knapsack(amount, pick_list,
                                              recursive=False)
                self.update_chips(pick)
                amount -= sum(pick)
            else:
                pick = pick_list[-1]
                self.update_chips(pick)
                amount -= pick

    def buy_chips(self, amount):
        self.chips.extend(self.get_chip_knapsack(amount, self.DENOMINATIONS))
        return self

    def bet_chips(self, amount):
        self.pull_from_knapsack(amount)
        return self

    def trade_chips(self, amount):
        value = self.bet_chips(amount)
        return value

    def update_chips(self, obj):
        if isinstance(obj, list):
            for item in obj:
                self.chips.remove(item)
        elif isinstance(obj, int):
            self.chips.remove(obj)
        else:
            return self
        return self


class Card:
    """Card class"""
    CARDS_dict = {
        'numerics': arange(2, 11), 'aces': array(['A']), 'faces':
            array(['k', 'Q', 'J']), 'suites': array(['Spades', 'Hearts',
                                                     'Diamonds', 'Clubs'])
    }

    def __init__(self):
        pass

    def draw_card(self):
        pass

    def get_card(self):
        pass


class Deck(Card):
    """ """

    def __init__(self):
        Card.__init__(self)
        self.deck = []
        self.cards = []

    def make_deck(self):
        """ Make a 52 card deck"""

        # combine all card types
        self.cards = concatenate([value for key, value in
                                   Card.CARDS_dict.items() if key !='suites'])
        # form a deck object
        self.deck = product(self.cards, Card.CARDS_dict['suites'])

        return list(self.deck)


class Player:
    """Class holds objects attributes and actions a player can take while
    playing a game of BlackJack against a computer.

    The following parameters are mandatory for creating a class instance.

    -`name` - Player's name, defaults to 'Player'
    -`balance` - Player's account balance, defaults
    to 0
    """

    def __init__(self, name='Player', balance=0):
        self.player_hand = []
        self.name = name
        self.balance = balance
        self.player_chips = Chip()

    def init_balance(self):
        get_balance = input(f"Please provide {self.name}'s bank balance: ")
        self.balance = int(get_balance)

    def chips(self):
        return self.player_chips.chips

    def deposit(self, amount):
        """Deposit winning proceeds"""
        self.balance += amount

    def withdraw(self, amount):
        self.balance += amount
        self.player_chips.trade_chips(amount)

    def buy(self, amount):
        """Buy a `quantity` amount worth of chips """
        if self.balance >= amount:
            self.balance -= amount
            self.player_chips.buy_chips(amount)
        else:
            print(f'Buying amount exceeds available funds: Available funds '
                  f'= {self.balance}')

    def bet(self, amount):
        """Place total amount to bet

        :param amount: betting amount
        :type amount: int
        :raise Exception: betting amount should be greater than available
        balance.
        """
        if sum(self.chips()) >= amount:
            self.balance -= amount
            self.player_chips.bet_chips(amount)
        else:
            print(f'Betting amount exceeds available chips: \nAvailable '
                  f'chips balance = {sum(self.chips())} \nAvailable '
                  f'bank balance '
                  f'= {self.balance}')
            player_decide = ' '
            undecided = True
            while undecided:
                player_decide = input('\nContinue to buying chips? [Y]/N: '
                                      '').lower()
                if player_decide == 'y' or player_decide == 'n':
                    undecided = False
                elif player_decide != 'y' or player_decide != 'n':
                    print("\nInvalid response: Only 'Y' or 'N' responses "
                          "accepted:")

            if player_decide == 'y':
                if self.balance >= amount:
                    print(f"I will continue and buy {amount} units worth "
                          f"more chips for you {self.name}")
                    self.buy(amount)
                    self.bet(amount)
                elif self.balance >= (amount-sum(self.chips())):
                    print(f"I will continue and buy "
                          f"{amount -sum(self.chips())} units worth "
                          f"more chips for you {self.name}")
                    self.buy(amount-sum(self.chips()))
                    self.bet(amount)
                else:
                    decide = input(f"\nInsufficient funds for the bet amount: "
                                   f"\nDeposit more funds into account or "
                                   f"Cashout ('Y' to deposit): ").lower()
                    final_decision = False
                    while not final_decision:
                        if decide == 'y' or decide == 'n':
                            final_decision = True
                        elif decide != 'y' or decide != 'n':
                            print("\nInvalid response: Only 'Y' or 'N' "
                                  "responses accepted:")
                            decide = input('\nPlease enter a valid option '
                                           'Y/N: ')
                            decide = decide.lower()

                    if decide == 'y':
                        deposit_amount = input('Please enter amount: ')
                        self.deposit(int(deposit_amount))
                        self.buy(amount)
                        self.bet(amount)

                    elif decide == 'n':
                        self.withdraw(sum(self.chips()))
            elif player_decide == 'n':
                self.withdraw(sum(self.chips()))

    def deposit_win(self, amount):
        """cash in the wins

        :param amount: amount won
        :type amount: float
        """
        self.player_chips.bet_chips(amount)
        self.balance += amount

    def hand(self):
        return self.player_hand

    def hit(self, card):
        self.player_hand.append(card)

    def stand(self):
        return self.player_hand

    def split(self):
        pass


class Dealer:
    """ """
    pass


class Game:

    def __init__(self, num_decks=6, num_players=3):
        self.players = []
        self.player_profiles = {}
        self.deck = Deck()
        self.num_decks = num_decks
        # number of players exclude dealer
        self.num_players = num_players
        self.game_deck = self.set_deck()

    def init_deal(self):
        """Initial hand deal before games begin"""
        for i in range(2):
            for gamer in self.player_profiles.keys():
                self.player_profiles[gamer].hit(self.draw_card())
        return self

    def get_players(self):
        while self.num_players:
            player_name = input(f'Insert player_{len(self.players) + 1}: ')
            self.players.append(player_name)
            self.num_players -= 1
        return self

    # get player profiles
    def get_profiles(self):
        self.get_players()
        for player in self.players:
            profile = Player(name=player)
            self.player_profiles[player] = profile
        return self

    def get_chips(self):
        for gamer in self.players:
            player_chips = input(f"Buying chips for {gamer}: ")
            self.player_profiles[gamer].buy(int(player_chips))
        return self

    def get_bets(self):
        for gamer in self.players:
            betting_chips = input(f"Betting amount for {gamer}: ")
            self.player_profiles[gamer].bet(int(betting_chips))
        return self

    def get_init_balances(self):
        for gamer in self.players:
            self.player_profiles[gamer].init_balance()
        return self

    def get_num_players(self):
        num_players = input("Please specify the number of players: ")
        self.num_players = int(num_players)
        return self

    def players_table(self):
        table = Texttable(0)
        for player in self.players:
            table.add_rows(
                [
                    ['Player Name', 'Hand', 'Bank Balance', 'Chips Balance'],
                    [
                        f'{player}', self.player_profiles[player].hand(),
                        self.player_profiles[player].balance,
                        sum(self.player_profiles[player].chips)
                    ]
                ])
        print(table.draw())

    def play(self):
        players_info = self.get_num_players()
        players_info.get_profiles().get_init_balances().get_chips().get_bets()
        #clear_screen()
        self.players_table()

    def shuffle_game_deck(self):
        game_deck = self.deck.make_deck() * self.num_decks
        # shuffle game deck in place
        shuffle(game_deck)
        return game_deck

    def draw_card(self):
        # draw out first card from deck and return the drawn card
        drawn = self.game_deck.pop(0)
        return drawn

    def set_deck(self):
        # set game deck
        return self.shuffle_game_deck()


if __name__ == '__main__':
    import pdb
    pdb.set_trace()
    game = Game()
    game.play()


