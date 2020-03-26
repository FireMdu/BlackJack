"""This script is a allows a single player to play a game of BlackJack
against a computer:

The rules have been dumbed down for ease of coding the game: More
functionality to be added in the future.
"""
import pdb


class Player:
    """Class holds objects attributes and actions a player can take while
    playing a game of BlackJack against a computer.

    The following parameters are mandatory for creating a class instance.

    -`name` - Player's name, defaults to 'Player'
    -`balance` - Player's account balance, defaults
    to 0
    """
    def __init__(self, name='Player', balance=0):
        self.name = name
        self.balance = balance

    def bet(self, amount):
        """Place total amount to bet

        :param amount: betting amount
        :type amount: float
        :raise Exception: betting amount should be greater than available
        balance.
        """
        if self.balance >= amount:
            self.balance -= amount
        else:
            print(f'Betting amount exceeds available funds: Available funds '
                  f'= {self.balance}')

    def deposit_win(self, amount):
        """cash in the wins

        :param amount: amount won
        :type amount: float
        """
        self.balance += amount


class Chip:
    """Class holds objects attributes of each chip denomination a player has.

        The following parameters are mandatory for creating a class instance.

        -`denomination` - Denomination number of the chip, defaults to 1
        -`balance` - Balance of the specified denomination, defaults to 0
        to 0
        """
    def __init__(self, denomination=1, balance=0):
        self.denomination = denomination
        self.balance = balance

    def place(self, quantity):
        """Place a `quantity` amount of chips of `self.denomination` id up
        for a bet."""
        if self.balance >= quantity:
            self.balance -= quantity
        else:
            raise Exception(f'Number of available chip denomination exceeded'
                            f'{self.denomination} funds: Available ='
                            f' {self.balance}')

    def deposit(self, quantity):
        """Deposit winning proceeds"""
        self.balance += quantity

    def buy(self, quantity):
        """Buy a `quantity` amount of chips of `self.denomination` id"""
        pass


class Card:
    """ """
    pass


class Dealer:
    """ """
    pass

if __name__ == '__main__':
    pdb.set_trace()
    Person = Player('Mdu')
    print(Person.balance)
