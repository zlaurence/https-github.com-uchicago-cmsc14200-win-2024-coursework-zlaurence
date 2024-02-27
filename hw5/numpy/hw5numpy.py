from abc import abstractmethod, ABC
from typing import Any

# type synonym for convenience
Shape = int | tuple[int, int]


class NDArray(ABC):
    """
    Abstract class for n-dimensional arrays
    """

    @property
    @abstractmethod
    def shape(self) -> Shape:
        """
        Return the shape of the data, either an int or a pair
        of ints in row, col order.

        Returns an int or a (row, col) pair of ints.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def data(self) -> list[int] | list[list[int]]:
        """
        Return *a defensive copy of* the data either as a list or
        list of lists.

        Don't return a reference to the actual data attribute
        itself so that it isn't subject to arbitrary modification.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def T(self) -> "NDArray":
        """
        Return the transpose of the data.

        Returns a 1D or 2D array. The tricky detail here is that
        in certain cases, an array changes dimension in
        transposition. The comments below address this.
        """
        raise NotImplementedError


class NDArray1(NDArray):
    """
    1-dimensional arrays
    """

    _data: list[int]
    _shape: Shape

    def __init__(self, data: list[int]):
        """
        Construct an NDArray1 from a list of int.
        """
        self._data = data
        self._shape = len(data)
        

    def __add__(self, other: Any) -> "NDArray1":
        """
        Add either an int or another NDArray1.
        Produce a new array (functional style).

        Raises Value error if other is neither an int nor
        and NDArray1, or an NDArray1 of different shape.
        """
        if isinstance(other, int):
            return NDArray1([x + other for x in self._data])
        elif isinstance(other, NDArray1) and self.shape == other.shape:
            result = []
            for i in range(len(self._data)):
                result.append(self._data[i] + other._data[i])
            return NDArray1(result)
        else:
            raise ValueError("Wrong Shape")

    def __gt__(self, other: Any) -> list[bool]:
        """
        Return a list of bools indicating greater than given int.
        """
        if not isinstance(other, int):
            raise ValueError("Must be an int.")
        return [x > other for x in self._data]


    def __contains__(self, other: Any) -> bool:
        """
        Test whether the given int is in the array.
        """
        return other in self._data

    def __eq__(self, other: Any) -> bool:
        """
        Test whether other is an NDArray1 with the same shape and
        containing the same numbers.
        """
        if isinstance(other, NDArray1) and self.shape == other.shape:
            return self._data == other._data
        return False

    @property
    def shape(self) -> Shape:
        """
        see NDArray
        """
        return self._shape

    @property
    def data(self) -> list[int] | list[list[int]]:
        """
        see NDArray
        """
        return self._data[:]

    @property
    def T(self) -> NDArray:
        """
        see NDArray

        Note the transpose of a size-n 1D array is an nx1 2D array.
        """
        return NDArray2([[x] for x in self._data])


class NDArray2(NDArray):
    """
    2-dimensional arrays
    """

    _data: list[list[int]]
    _shape: Shape

    def __init__(self, data: list[list[int]]):
        """
        Construct an NDArray2 from a list of lists of int.

        Raises ValueError if list of lists is jagged (not
        rectangular).
        """
        if any(len(row) != len(data[0]) for row in data):
            raise ValueError("Array must be rectangular.")
        self._data = data
        self._shape = (len(data), len(data[0]))

    def __add__(self, other: Any) -> "NDArray2":
        """
        Add either an int or another NDArray2.
        Produce a new array (functional style).

        Raises Value error if other is neither and int nor an
        NDArray2, or an NDArray2 of different shape.
        """
        if isinstance(other, int):
            return NDArray2([[x + other for x in row] for row in self._data])
        elif isinstance(other, NDArray2) and self.shape == other.shape:
            result = []
            for i in range(len(self._data)):
                row = []
                for j in range(len(self._data[i])):
                    row.append(self._data[i][j] + other._data[i][j])
                result.append(row)
            return NDArray2(result)
        else:
            raise ValueError("Operand must be an int or NDArray2 of the same shape.")

    def __gt__(self, other: Any) -> list[list[bool]]:
        """
        Return a list of lists of flags indicating greater than
        given int.
        """
        if not isinstance(other, int):
            raise ValueError("Operand must be an int.")
        return [[x > other for x in row] for row in self._data]

    def __contains__(self, other: Any) -> bool:
        """
        Test whether the given int is anywhere in the array.
        """
        return any(other in row for row in self._data)

    def __eq__(self, other: Any) -> bool:
        """
        Test whether other is an NDArray2 with the same shape and
        containing the same numbers.
        """
        if isinstance(other, NDArray2) and self.shape == other.shape:
            return self._data == other._data
        return False
    @property
    def shape(self) -> Shape:
        """
        see NDArray
        """
        return self._shape

    @property
    def data(self) -> list[int] | list[list[int]]:
        """
        see NDArray
        """
        return [row[:] for row in self._data]

    @property
    def T(self) -> NDArray:
        """
        see NDArray

        Note the transpose of an nx1 2D array is a size-n 1D array.
        """
        num_cols = len(self._data[0])
        transposed_data = [[] for _ in range(num_cols)]
        for row in self._data:
            for j, elem in enumerate(row):
                transposed_data[j].append(elem)
        if len(transposed_data) == 1:
            return NDArray1(transposed_data[0])
        else:
            return NDArray2(transposed_data)
