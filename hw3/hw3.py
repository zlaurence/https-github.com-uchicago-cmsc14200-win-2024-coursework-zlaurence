"""
CMSC 14200, Spring 2024
Homework #3

People Consulted:
   List anyone (other than the course staff) that you consulted about
   this assignment.

Online resources consulted:
   List the URLs of any online resources other than the course text and
   the official Python language documentation that you used to complete
   this assignment.
"""

from typing import Optional, Literal
from graphs import Graph, AdjacencyListDigraph, AdjacencyMatrixDigraph

def like_component(g: Graph, src: str) -> set[str]:
    """
    Computes and returns the connected component originating
    at src such that the value associated with each vertex
    is the same.

    Inputs:
      g (graph)
      src (str) a vertex label

    Returns:
      a set of strings, the labels of vertices in the component
    """
    if src not in g.vertex_labels:
        raise ValueError(f"The vertex {src} is not in the graph.")

    like = set([src])
    stack = [src]
    value = g.get_value(src)

    while stack:
        vertex = stack.pop()
        for neigh in g.out_neighbors(vertex):
            if g.get_value(neigh) == value and neigh not in like:
                like.add(neigh)
                stack.append(neigh)

    return like

Stone = Literal['BLACK']|Literal['WHITE']

class GoBoard:
    """ Class for representing Go boards """

    _size:  int
    _board: list[list[Optional[Stone]]]

    def __init__(self, size: int):
        """
        Inputs:
          size (int), the number of positions in each column and row
        """
        if size<2:
            raise ValueError('too small for Go')
        self._size = size
        self._board = [[]] * size
        for i in range(size):
            self._board[i] = [None] * size

    @property
    def size(self) -> int:
        """
        The side length of the Go board.

        Inputs: (nothing)

        Returns:
          the side length
        """
        return self._size

    def put(self, col: int, row: int, s: Stone) -> None:
        """
        Place a stone on the board. Overwrite whatever is there.

        Inputs:
          col (int), the target column
          row (int), the target row
          s (Stone), either 'BLACK' or 'WHITE'

        Returns: (nothing)
        """
        self._board[col][row] = s

    def get(self, col: int, row: int) -> Optional[Stone]:
        """
        Retrieve a stone, or None, from the designated location.

        Inputs:
          col (int), the target column
          row (int), the target row

        Returns:
          an Optional Stone
        """
        return self._board[col][row]

def go_graph(gb: GoBoard) -> Graph:
    """
    Given a Go board, construct a graph such that each
    board location is a vertex in the graph, all of that
    location's orthogonal neighbors are connected by an
    edge, and an optional stone is stored as the value at
    each location's vertex.

    Inputs:
      gb: a GoBoard object

    Returns:
      a graph as described
    """
    size = gb.size
    graph = AdjacencyListDigraph([f'{col}:{row}' for col in range(size) \
                                  for row in range(size)])
    
    for col in range(size):
        for row in range(size):
            
            cur_label = f'{col}:{row}'
            cur_value = gb.get(col, row)
            graph.set_value(cur_label, cur_value)

            
            if col < size - 1:
                r_label = f'{col + 1}:{row}'
                graph.connect(cur_label, r_label)
                graph.connect(r_label, cur_label)
            
           
            if row < size - 1:
                bot_label = f'{col}:{row + 1}'
                graph.connect(cur_label, bot_label)
                graph.connect(bot_label, cur_label)

    return graph
