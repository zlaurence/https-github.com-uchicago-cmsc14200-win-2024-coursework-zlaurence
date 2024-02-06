"""
CMSC 14200, Winter 2024
Homework #2

People Consulted:
   List anyone (other than the course staff) that you consulted about
   this assignment.

Online resources consulted:
   List the URLs of any online resources other than the course text and
   the official Python language documentation that you used to complete
   this assignment.
"""

from typing import Optional
from trees import StrExp, BSTNode, BSTEmpty, BaseBST



#### Task 1 ####
class StrNode(StrExp):
    """
    Class to represent a String node in an expression tree
    """
    s: str 
    def __init__(self, s: str):
        self.s = s

    def is_const(self) -> bool:
        return True

    def num_nodes(self) -> int:
        return 1

    def eval(self) -> str:
        return self.s

    def __str__(self) -> str:
        return f'"{self.s}"'


class Concat(StrExp):
    """
    Class to represent the "concatenation" operator
    """
    s1: "StrNode|Concat|Slice|Replace"
    s2: "StrNode|Concat|Slice|Replace"
    
    def __init__(self, s1: "StrNode|Concat|Slice|Replace", \
                 s2:"StrNode|Concat|Slice|Replace") -> None:
        self.s1 = s1
        self.s2 = s2
    def is_const(self) -> bool:
       return False
    def eval(self) -> str:
       return self.s1.eval() + self.s2.eval()
    def num_nodes(self) -> int:
        return 1 + self.s1.num_nodes() + self.s2.num_nodes()
    def __str__(self) -> str:
       return f'Concat({self.s1}, {self.s2})'

class Slice(StrExp):
    """
    Class to represent the "slice" operator
    """
    s: "StrNode|Concat|Slice|Replace"
    low: int
    high: int
    step: int

    def __init__(self, s: "StrNode|Concat|Slice|Replace", \
                 low: int, high: int, step:int) -> None:
        self.s = s
        self.low = low 
        self.high = high
        self.step = step
    def is_const(self) -> bool:
        return False
    def num_nodes(self) -> int:
        return 1 + self.s.num_nodes()
    def eval(self) -> str:
        string_value = self.s.eval()
        return string_value[self.low:self.high:self.step]
    def __str__(self) -> str:
        return f'Slice({self.s}, {self.low}, {self.high}, {self.step})'


class Replace(StrExp):
    """
    Class to represent the "replace" operator
    """
    s: "StrNode|Concat|Slice|Replace"
    badstr: "StrNode|Concat|Slice|Replace"
    newstr: "StrNode|Concat|Slice|Replace"
    def __init__(self, s: "StrNode|Concat|Slice|Replace", badstr: \
                 "StrNode|Concat|Slice|Replace", newstr: \
                    "StrNode|Concat|Slice|Replace") -> None:
        self.s = s
        self.badstr = badstr 
        self.newstr = newstr
    def eval(self) -> str:
        return self.s.eval().replace(self.badstr.eval(), self.newstr.eval())
    def is_const(self) -> bool:
        return False
    def num_nodes(self) -> int:
        return 1 + self.s.num_nodes() + self.badstr.num_nodes()\
              + self.newstr.num_nodes()
    def __str__(self) -> str:
        return f"Replace({self.s}, {self.badstr}, {self.newstr})"
#### Task 2 ####

def valid_bst(tree: BaseBST) -> bool:
    """
    Determine whether or not a tree respects the BST ordering property

    Input:
        t (BST): the tree

    Returns (bool): True if t is a properly-ordered BST, False otherwise
    """
    if tree.is_empty:
        return True

    stack = [(tree, None, None)]  

    while stack:
        node, lower, upper = stack.pop()
        if (lower is not None and node.value <= lower) or \
            (upper is not None and node.value >= upper):
            return False
        if not node.right.is_empty:
            stack.append((node.right, node.value, upper))
        if not node.left.is_empty:
            stack.append((node.left, lower, node.value))
    return True

#### Task 3 ####

class BSTEmptyOpt:
    """
    Empty (Optimized) BST Tree
    """

    # No constructor needed (nothing to initialize)

    @property
    def is_empty(self) -> bool:
        """
        Returns: True if the tree is empty, False otherwise
        """
        return True

    @property
    def is_leaf(self) -> bool:
        """
        Returns: True if the tree is a leaf node, False otherwise
        """
        return False

    @property
    def num_nodes(self) -> int:
        """
        Returns: The number of nodes in the tree
        """
        return 0

    @property
    def height(self) -> int:
        """
        Returns: The height of the tree
        """
        return 0

    @property
    def span(self) -> Optional[tuple[int, int]]:
        """
        Returns: A tuple with the min and max value in the tree;
                 None for an empty tree
        """
        return None

    def contains(self, n: int) -> bool:  
        """
        Determines whether a value is contained in the tree.

        Args:
            n: The value to check

        Returns: True if the value is contained in the tree,
            False otherwise.
        """
        return False

    def insert(self, n: int) -> "BSTNodeOpt":
        """
        Inserts a value into the tree

        Args:
            n: Value to insert

        Returns: A new tree with the value inserted into it
        """
        return BSTNodeOpt(n, BSTEmptyOpt(), BSTEmptyOpt())


class BSTNodeOpt:
    """
    (Optimized) BST Tree Node
    """

    value: int
    left: "BSTEmptyOpt | BSTNodeOpt"
    right: "BSTEmptyOpt | BSTNodeOpt"
    

    def __init__(self, n: int,
                 left: "BSTEmptyOpt | BSTNodeOpt",
                 right: "BSTEmptyOpt | BSTNodeOpt"):
        """
        Constructor

        Args:
            n: Value associated with the tree node
            left: Left child tree
            right: Right child tree
        """
        self.value = n
        self.left = left
        self.right = right
        self._span = (n, n)
        self.update_span()

    @property
    def is_empty(self) -> bool:
        """
        Returns: True if the tree is empty, False otherwise
        """
        return False

    @property
    def is_leaf(self) -> bool:
        """
        Returns: True if the tree is a leaf node, False otherwise
        """
        return self.left.is_empty and self.right.is_empty

    @property
    def num_nodes(self) -> int:
        """
        Returns: The number of nodes in the tree
        """
        return 1 + self.left.num_nodes + self.right.num_nodes

    @property
    def height(self) -> int:
        """
        Returns: The height of the tree
        """
        return 1 + max(self.left.height, self.right.height)
    def update_span(self):
        """
        Updates the span for node
        """
        # Span of left and right children
        left_span = self.left.span if not self.left.is_empty else \
            (self.value, self.value)
        right_span = self.right.span if not self.right.is_empty else \
            (self.value, self.value)
        # Update the current span
        self._span = (min(left_span[0], self.value, right_span[0]), \
                      max(left_span[1], self.value, right_span[1]))

    @property
    def span(self) -> Optional[tuple[int, int]]:
        """
        Returns: A tuple with the min and max value in the tree;
                 None for an empty tree
        """
        return self._span

    @property
    def balance_factor(self) -> int:
        """
        Returns: Balance factor of the tree
        """
        return self.right.height - self.left.height

    def contains(self, n: int) -> bool:
        """
        Determines whether a value is contained in the tree.

        Args:
            n: The value to check

        Returns: True if the value is contained in the tree,
            False otherwise.
        """
        if n < self._span[0] or n > self._span[1]:
            return False
        if n < self.value:
            return self.left.contains(n)
        elif n > self.value:
            return self.right.contains(n)
        else:
            return True

    def insert(self, n: int) -> "BSTNodeOpt":
        """
        Inserts a value into the tree

        Args:
            n: Value to insert

        Returns: A new tree with the value inserted into it
        """
        if n < self.value:
            self.left = self.left.insert(n)
        elif n > self.value:
            self.right = self.right.insert(n)
        
        self.update_span()
        return self


#### Task 4 ####

class Board:
    """
    Class to represent a game board.

    Attributes:
        rows (int): number of rows
        cols (int): number of columns
        board (list): the game board
        location_of_pieces (dictionary): the location of each piece
          on the board

    Methods:
        add_piece: add a piece represented by a string to the board
    """
    rows: int
    cols: int
    board: list[list[Optional[str]]]

    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        self.board = [[None] * cols for _ in range(rows)]

    def add_piece(self, piece: str, location: tuple[int, int]) -> bool:
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
            return True
        return False

    # Add your dominating property here
    @property
    def dominating(self) -> Optional[str]:
        """
        This function returns the peice that is dominating the most, if there
        is one.

        Input:
            Self
        Return: String or None
        """
        piece_count = {}
        for row in self.board:
            for cell in row:
                if cell:
                    piece_count[cell] = piece_count.get(cell, 0) + 1

        max_pieces = max(piece_count.values(), default=0)
        max_pieces_list = [piece for piece, count in piece_count.items() \
                           if count == max_pieces]
        if len(max_pieces_list) == 1:
            return max_pieces_list[0] 
        else:
            return None

