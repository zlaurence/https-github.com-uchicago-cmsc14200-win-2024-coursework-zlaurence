"""
CMSC 14200, Winter 2024
Homework #1

People Consulted:
   List anyone (other than the course staff) that you consulted about
   this assignment.

Online resources consulted:
   List the URLs of any online resources other than the course text and
   the official Python language documentation that you used to complete
   this assignment.
"""

from typing import Optional
from abc import ABC, abstractmethod
from tree import TreeNode

def count_words(list_of_strings: list[str], starts_with: str) -> dict[str, int]:
    """
    Find the words that start with a given substring and count the number of
    times each word appears.

    Inputs:
        list_of_strings (list): the list of words
        starts_with (string): substring that has to appear in each word

    Returns (dict): the words and counts of each word that starts with the given
    """
    rv = {}
    for strings in list_of_strings:
        if starts_with in strings:
            if strings not in rv:
                rv[strings] = 1
            elif strings in rv:
                rv[strings] +=1
    return rv
class Board:
    """
    Class to represent a game board.

    Attributes:
        rows (int): number of rows
        cols (int): number of columns
        board (list): the game board
        location_of_pieces (dictionary): the location of each piece on the board

    Methods:
        add_piece: add a piece represented by a string to the board
    """
    board: list[list[Optional[str]]]
    location_of_pieces: dict[Optional[str], list[tuple[int,int]]]

    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        self.board = [[None] * cols for _ in range(rows)]
        self.location_of_pieces = {}

    def add_piece(self, piece: str, location: tuple[int,int]) -> bool:
        """
        Add a piece represented by a string to the board.

        Inputs:
            piece (string): the piece to add
            location (tuple): the (row, column) location of where to add
                the piece

        Returns (bool): True if the piece was added successfully,
            False otherwise
        """
        row, col = location
        if self.board[row][col] is None:
            self.board[row][col] = piece
            if piece in self.location_of_pieces:
                self.location_of_pieces[piece].append(location)
            else:
                self.location_of_pieces[piece] = [location]
            return True
        return False

def get_all_paths(t: TreeNode) -> list[list[int]]:
    """
    Find all the unique paths from the root to a leaf node in a tree.

    Inputs:
        t (TreeNode): the tree

    Returns (list): the list of paths
    """
    all_paths: list[list[int]] = []
    if not t.children:
        return [[t.value]]
    for child_path in t.children:
        for path in get_all_paths(child_path):
            all_paths.append([t.value]+ path)
    return all_paths

class InsufficientFundsError(Exception):
    """
    Exception to be raised when an account has insufficient funds
    """
    pass

class Account(ABC):
    """
    Class to represent a bank account.

    Methods:
        deposit: deposit money into the account
        withdraw: withdraw money from the account

    Property:
        balance: the balance of the account
    """

    def __init__(self, account_number: int, balance: float = 0):
        self.account_number = account_number # got rid of an underscore
        self.balance = float(balance)

    @abstractmethod
    def deposit(self, amount: float) -> None:
        """
        Makes a deposit in the account.

        Inputs:
            amount (float): Amount to deposit

        Returns: Nothing
        """
        self.balance += amount

    @abstractmethod
    def withdraw(self, amount: float) -> float:
        """
        Makes a withdrawal from the account.

        Inputs:
            amount (float): Amount to withdraw

        Returns (float): Withdrawn amount.
        """
        if self.balance <= amount:
            self.balance = 0
        else:
            self.balance -= amount
        return amount
    @property
    @abstractmethod
    def balance(self) -> float:
        """
        Returns the balance of the account

        Returns (float): Account balance
        """
        return self.balance
        raise NotImplementedError
class SavingsAccount(Account):
    """
    Class to represent a savings account
    """
    def __init__(self, account_number: int, balance: float = 0):
        """See docstring in Account.__init__"""
        super().__init__(account_number, balance)

    def deposit(self, amount: float) -> None:
        """
        See docstring in Account.deposity
        """
        return super().deposit(amount)
    def withdraw(self, amount: float) -> float:
        """
        Uses super withdraw function
        takes amount and subtracts from balance while checking if funds are 
        posative
        """
        if amount > self.balance:
            raise InsufficientFundsError("Insufficient funds")
        return super().withdraw(amount)
    def balance(self) -> float:
        """
        Use Super balance function
        to return balance"""
        return super().balance()
class CheckingAccount(Account): #how do I get overdraft limit in here?
    """
    Class to represent a checking account
    """
    def __init__(self, account_number: int, balance: float = 0,\
                  overdraft_limit: float = 0):
        super().__init__(account_number, balance)
        self.overdraft_limit = overdraft_limit
        self.amount_overdrawn = 0
    def deposit(self, amount: float) -> None:
        """ 
        Uses super deposit function
        takes in amount and modifies balance 
        """
        if amount < self.amount_overdrawn:
            self.amount_overdrawn -= amount
            return 0.0
        if amount > self.amount_overdrawn:
            add = amount - self.amount_overdrawn
            self.amount_overdrawn = 0
            return super().deposit(add)
        return super().deposit(amount)
    @property
    def available_overdraft(self):
        """returns how much the acount can be overdrawn by"""
        return self.overdraft_limit - self.amount_overdrawn

    def withdraw(self, amount: float) -> float:
        """withdraws from balance if there are sufficient funds and allows for 
        overdrafting
        """
        if amount > self.balance:
            if amount > (self.overdraft_limit \
                         - self.amount_overdrawn + self.balance):
                raise InsufficientFundsError("Insufficient funds")
            self.amount_overdrawn = self.amount_overdrawn + \
                self.overdraft_limit + self.balance - amount
            self.balance = 0.0
        return super().withdraw(amount)
    def balance(self, amount: float) -> float:
        """Uses super balance function"""
        return super().balance(amount)
class HighYieldSavingsAccount(SavingsAccount):
    """
    Class to represent a high yeild savings account
    """
    def __init__(self, account_number: int, balance: float = 0,\
                  min_balance: float = 0, rate: float = 0):
        """Initializes variables from super"""
        super().__init__(account_number, balance)
        self.min_balance = min_balance
        self.rate = rate
    def withdraw(self, amount: float) -> float:
        """
        Makes a withdrawal from the account.

        Inputs:
            amount (float): Amount to withdraw

        Returns (float): Withdrawn amount.
        """
        if self.min_balance > self.balance - amount:
            raise InsufficientFundsError\
                ("Withdrawal exceeds minimum balance threshold")
        return super().withdraw(amount)
    def deposit(self, amount: float) -> None:
        """See doc string in Account.deposity """
        return super().deposit(amount)
    def add_monthly_interest(self) -> None:
        """Adds monthly intrest
        Multiplies balance by monthly rate and updates balance"""
        interest_owed = self.balance * self.rate
        self.balance += interest_owed
    def balance(self, amount: float) -> float:
        """Uses super balance function"""
        return super().balance(amount)
