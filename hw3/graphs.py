"""
CMSC 14200, Spring 2024
Homework #3
"""
from abc import ABC, abstractmethod
from typing import Any, Optional

class Graph(ABC):
    """ Abstract class for graphs """

    @property
    @abstractmethod
    def num_vertices(self) -> int:
        """
        Inputs: (nothing)

        Returns: the number of vertices in the graph.
        """
        raise NotImplementedError


    @property
    @abstractmethod
    def num_edges(self) -> int:
        """
        Inputs: (nothing)

        Returns: the number of edges in the graph.
        """

        raise NotImplementedError
    @property
    @abstractmethod
    def vertex_labels(self) -> set[str]:
        """
        Inputs: (nothing)

        Returns: the set of all vertex labels in the graph.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def edges(self) -> set[tuple[str, str]]:
        """
        Inputs: (nothing)

        Returns: the set of all edges in the graph. Each edge is a
        tuple of labels in (source, destination) order.
        """
        raise NotImplementedError


    @abstractmethod
    def connect(self, src: str, dst: str) -> None:
        """
        Adds an edge to the graph.

        Inputs:
           src, the label of the origin of the new edge
           dst, the label of the destination of the new edge

        Returns: (nothing)

        Raises:
            ValueError if src or dst not in the graph
        """
        raise NotImplementedError



    @abstractmethod
    def connected(self, src: str, dst: str) -> bool:
        """
        Inputs:
           src, the label of the origin of the new edge
           dst, the label of the destination of the new edge

        Returns: True is there is such an edge, False otherwise

        Raises:
            ValueError if src or dst not in the graph
        """
        raise NotImplementedError

    @abstractmethod
    def out_neighbors(self, src: str) -> set[str]:
        """
        Returns the set of the labels of all vertices
        directly connected to src by an edge originating
        at src.

        Inputs:
          src, a vertex label

        Returns: a set of strings

        Raises:
            ValueError if src not in the graph
        """
        raise NotImplementedError

    @abstractmethod
    def get_value(self, vertex: str) -> Any:
        """
        Return the value associated with a vertex.

        Inputs:
          vertex, a label

        Returns: the value at the chosen vertex.

        Raises:
            ValueError if vertex not in the graph
        """
        raise NotImplementedError

    @abstractmethod
    def set_value(self, vertex: str, value: Any) -> None:
        """
        Set the value at the chosen vertex to what is given,
        overwriting whatever value was already present.

        Inputs:
          vertex, a label
          value, a value of any kind of data

        Returns: (nothing)

        Raises:
            ValueError if vertex not in the graph
        """
        raise NotImplementedError

    @abstractmethod
    def to_adj_list(self) -> 'AdjacencyListDigraph':
        """
        Return the same graph in adjacency list form.

        Inputs: (nothing)

        Returns: an AdjacencyListDigraph.
        """
        raise NotImplementedError

    @abstractmethod
    def to_adj_matrix(self) -> 'AdjacencyMatrixDigraph':
        """
        Return the same graph in adjacency matrix form.

        Inputs: (nothing)

        Returns: an AdjacencyMatrixDigraph.
        """
        raise NotImplementedError
    

class AdjacencyListDigraph(Graph):
    """ Adjacency list implementation of graphs """

    _neighbors:     dict[str,list[str]]
    _vertex_values: dict[str,Any]

    def __init__(self, vertex_labels:list[str]):
        super().__init__()
        self._neighbors = {}
        self._vertex_values = {}
        for vertex in vertex_labels:
                self._neighbors[vertex] = []
                self._vertex_values[vertex] = None
       
    @property
    def num_vertices(self):
        return len(self._neighbors)
    @property
    def num_edges(self):
        return sum(len(neigh) for neigh in self._neighbors.values())
    @property
    def vertex_labels(self):
        return set(self._vertex_values.keys())
    @property
    def edges(self):
        edge_set = set()
        for src, neigh in self._neighbors.items():
            for dst in neigh:
                edge_set.add((src,dst))
        return edge_set


    def connect(self, src, dst):
        if src not in self._vertex_values:
            raise ValueError(f"Source vertex {src} does not exist.")
        if dst not in self._vertex_values:
            raise ValueError(f"Destination vertex {dst} does not exist.")
        self._neighbors[src].append(dst)
   
    def connected(self, src, dst):
        if src not in self._neighbors:
            raise ValueError("Source vertex not in the graph")
        if dst not in self._neighbors:
            raise ValueError("Destination vertex not in the graph")
        return dst in self._neighbors.get(src, [])
    
    def out_neighbors(self, src):
       return set(self._neighbors.get(src,[]))

    
    def get_value(self, vertex):
        if vertex not in self._vertex_values:
            raise KeyError(f"Vertex '{vertex}' does not exist in the graph.")
        return self._vertex_values.get(vertex)
    
    def set_value(self, vertex, value):
        if vertex not in self._vertex_values:
            raise KeyError(f"Vertex '{vertex}' does not exist in the graph.")
        self._vertex_values[vertex] = value

    def to_adj_list(self):
        return self
    
    def to_adj_matrix(self):
        matrix_graph = AdjacencyMatrixDigraph(self.vertex_labels)

        for src in self._neighbors:
            for dst in self._neighbors[src]:
                matrix_graph.connect(src, dst)

        return matrix_graph

class AdjacencyMatrixDigraph(Graph):
    """ Adjacency matrix implementation of graphs """

    _labels_to_ints: dict[str, int]
    _ints_to_labels: list[str]
    _adjacency:      list[list[bool]]
    _vertex_values:  dict[str, Any]

    def __init__(self, vertex_labels: list[str]):
        super().__init__()
        self._vertex_values = {}
        self._labels_to_ints = {}
        self._ints_to_labels = vertex_labels

        for index, label in enumerate(vertex_labels):
            self._vertex_values[label] = None
            self._labels_to_ints[label] = index

        size = len(vertex_labels)
        self._adjacency = [[False] * size for _ in range(size)]


    @property
    def num_vertices(self):
       return len(self._adjacency)
    @property
    def num_edges(self):
        """
        Calculate the  number of edges in the graph.
        int: The total number of edges in the graph.
        """
        edge_count = 0
        for row in self._adjacency:
            edge_count += sum(row)  
        return edge_count
    @property
    def vertex_labels(self):
        return set(self._ints_to_labels)
    @property
    def edges(self):
        edge_set = set()
        for i, Rows in enumerate(self._adjacency):
            for j, con in enumerate(Rows):
                if con:
                    src = self._ints_to_labels[i]
                    dst = self._ints_to_labels[j]
                    edge_set.add((src, dst))
        return edge_set
    def connect(self, src, dst):
        """Connect two points """
        if src not in self._labels_to_ints or dst not in self._labels_to_ints:
            raise ValueError

        i, j = self._labels_to_ints[src], self._labels_to_ints[dst]
        self._adjacency[i][j] = True
    
    def connected(self, src, dst):
        if src not in self._labels_to_ints:
            raise ValueError(f"Source vertex '{src}' not in the graph")
        if dst not in self._labels_to_ints:
            raise ValueError(f"Destination vertex '{dst}' not in the graph")

        src_index = self._labels_to_ints[src]
        dst_index = self._labels_to_ints[dst]
        return self._adjacency[src_index][dst_index]

    def out_neighbors(self,src: str):
        if src not in self._labels_to_ints:
            raise KeyError(f"Vertex '{src}' does not exist in the graph.")

        src_index = self._labels_to_ints[src]
        neighbors = set()
        for j, con in enumerate(self._adjacency[src_index]):
            if con:
                neighbors.add(self._ints_to_labels[j])
        return neighbors

    def get_value(self, vertex):
       if vertex not in self._vertex_values:
            raise KeyError(f"Vertex '{vertex}' does not exist in the graph.")
       return self._vertex_values.get(vertex)
    
    def set_value(self, vertex, value):
       if vertex not in self._vertex_values:
            raise KeyError(f"Vertex '{vertex}' does not exist in the graph.")
       self._vertex_values[vertex] = value

    def to_adj_list(self) -> 'AdjacencyListDigraph':
        adj_list_graph = AdjacencyListDigraph(self._ints_to_labels)
        for i, row in enumerate(self._adjacency):
            src = self._ints_to_labels[i]
            for j, con in enumerate(row):
                if con:
                    dst = self._ints_to_labels[j]
                    adj_list_graph.connect(src, dst) 
        return adj_list_graph
    
    def to_adj_matrix(self) -> 'AdjacencyMatrixDigraph':
        return self
    
