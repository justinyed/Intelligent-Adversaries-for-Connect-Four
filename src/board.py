import copy
from ast import literal_eval
import numpy as np
import io
import sys

HEIGHT = 6
WIDTH = 7
DEFAULT = 0
N_CONNECT = 4
X = 0
Y = 1


class BoardInterface:
    """The Internal Representation of a Grid Style Board."""

    def __init__(self, height=HEIGHT, width=WIDTH, default=DEFAULT, grid=None):
        """
        constructor for board object

        :param height: of the board
        :param width: of the board
        :param default: integer value for an empty space
        :param grid: if one wants to copy an existing board
        """

        self.height = height
        self.width = width
        self.default = default

        if grid is None:
            self.grid = self.new_grid()
        else:
            self.grid = grid

    def copy(self):
        """
        Perform Deep Copy

        :return: copy
        """
        pass

    def new_grid(self):
        """
        initialize the grid

        :return: New Grid
        """
        pass

    def get_grid(self):
        """
        get shallow copy of grid

        :return: internal grid
        """
        return self.grid

    def get_grid_copy(self):
        """
        get deep copy of grid

        :return: deep copy of internal grid
        """
        pass

    def set_grid(self, grid):
        """
        set internal grid

        :param grid: internal grid
        """
        self.grid = grid

    def set_piece(self, position, piece):
        """
        set piece in grid

        :param position: Tuple (x, y) of position to place piece
        :param piece: piece to place
        """
        pass

    def get_piece(self, position):
        """
        get piece at position in grid

        :param position: Tuple (x, y) of position to get
        :return: piece at position
        """
        pass

    def drop_piece(self, column, piece):
        """
        drop piece into slot in grid

        :param column: column to drop piece
        :return: new status after action
        """
        for y in range(self.height):
            position = (column, y)
            if self.get_piece(position) == self.default:
                self.set_piece(position, piece)
                return position

    def get_legal_actions(self):
        """
        :return: a generator which contains the legal moves
        """
        return (x for x in range(self.width) if self.get_piece((x, self.height - 1)) == self.default)

    def check_win(self, drop_position, current_piece):
        """
        Local Win Check. Checks Starting from the dropped piece (change on grid)
        :param current_piece: current piece
        :param drop_position: Position of Dropped Piece
        :return: True if Win was found, otherwise False
        """
        return self.__check_line(drop_position, (0, 1), current_piece) or \
               self.__check_line(drop_position, (1, 0), current_piece) or \
               self.__check_line(drop_position, (1, 1), current_piece) or \
               self.__check_line(drop_position, (-1, 1), current_piece)

    def __check_line(self, origin, direction, current_piece):
        return self.__count_line(origin, direction, current_piece) >= N_CONNECT

    def __count_line(self, origin, direction, current_piece):
        current_position = origin
        dx, dy = direction
        count = 0

        while self.is_legal_position(current_position) and self.__is_same_as_current(current_position, current_piece):
            current_position = current_position[X] + -1 * dx, current_position[Y] + -1 * dy

        current_position = current_position[X] + dx, current_position[Y] + dy

        while self.is_legal_position(current_position) and self.__is_same_as_current(current_position, current_piece):
            current_position = current_position[X] + dx, current_position[Y] + dy
            count += 1
        return count

    def __is_same_as_current(self, position, current_piece):
        return current_piece == self.get_piece(position)

    def is_legal_position(self, position):
        return 0 <= position[X] < self.width and 0 <= position[Y] < self.height

    def __hash__(self):
        return self.__str__()

    def __str__(self):
        return str(self.grid)


class TupleBoard(BoardInterface):
    """
    The Internal Representation of a Grid Style Board Game.
    """

    def __init__(self, grid=None, default=DEFAULT, height=HEIGHT, width=WIDTH):
        super().__init__(grid=grid, default=default, height=height, width=width)

    def new_grid(self):
        """
        Initialize the Grid
        :return: New Grid
        """
        return tuple((self.default
                      for _ in range(self.width * self.height)))

    def get_grid(self):
        """
        :return: internal grid
        """
        return self.grid

    def get_grid_copy(self):
        return copy.deepcopy(self.grid)

    def copy(self):
        return TupleBoard(grid=copy.deepcopy(self.get_grid()), height=copy.deepcopy(self.height), width=copy.deepcopy(self.width))

    def __copy__(self):
        return TupleBoard(grid=self.get_grid(), height=self.height, width=self.width)

    def __deepcopy__(self, memo):
        return TupleBoard(grid=copy.deepcopy(self.get_grid(), memo), height=copy.deepcopy(self.height, memo), width=copy.deepcopy(self.width, memo))

    def set_grid(self, grid):
        """
        Set internal grid
        :param grid: internal grid
        """
        self.grid = grid

    def set_piece(self, position, piece):
        """
        :param position: Tuple (x, y) of position to place piece
        :param piece: piece to place
        """
        x, y = position
        index = x + self.width * y
        self.grid = self.grid[:index] + (piece,) + self.grid[index + 1:]

    def get_piece(self, position):
        """
        :param position: Tuple (x, y) of position to get
        :return: piece at position
        """
        x, y = position
        return self.grid[x + self.width * y]

    def serialize(self):
        """
        serialize board to be stored

        :return: serialized board
        """
        return f"{self.height},{self.width},{self.default},{self.grid}"

    def load(self, serialized_object):
        """
        load board from serialized board

        """
        o = serialized_object.split(',')
        self.height = int(o[0])
        self.width = int(o[1])
        self.default = int(o[2])
        self.default = literal_eval(o[3])


class ArrayBoard(BoardInterface):
    """
    The Internal Representation of a Grid Style Board Game.
    """

    def __init__(self, grid=None, default=DEFAULT, height=HEIGHT, width=WIDTH):
        super().__init__(grid=grid, default=default, height=height, width=width)

    def new_grid(self):
        """
        Initialize the Grid
        :return: New Grid
        """
        return np.zeros((self.height, self.width), dtype=np.int8)

    def get_grid(self):
        """
        :return: internal grid
        """
        return self.grid

    def get_grid_copy(self):
        return np.copy(self.grid)

    def copy(self):
        return ArrayBoard(grid=np.copy(self.get_grid()), height=copy.deepcopy(self.height), width=copy.deepcopy(self.width))

    def __copy__(self):
        return ArrayBoard(grid=self.get_grid(), height=self.height, width=self.width)

    def __deepcopy__(self, memo):
        return ArrayBoard(grid=np.copy(self.get_grid()), height=copy.deepcopy(self.height, memo), width=copy.deepcopy(self.width, memo))

    def set_grid(self, grid):
        """
        Set internal grid
        :param grid: internal grid
        """
        self.grid = grid

    def set_piece(self, position, piece):
        """
        :param position: Tuple (x, y) of position to place piece
        :param piece: piece to place
        """
        self.grid[abs(position[Y] - (self.height - 1))][position[X]] = piece

    def get_piece(self, position):
        """
        :param position: Tuple (x, y) of position to get
        :return: piece at position
        """
        return self.grid[abs(position[Y] - (self.height - 1))][position[X]]

    def __hash__(self):
        return tuple(self.grid.flatten())


class BitBoard(BoardInterface):
    """
    The Internal Representation of a Grid Style Board Game.
    """

    def __init__(self, grid=None, default=DEFAULT, height=HEIGHT, width=WIDTH):
        super().__init__(grid=grid, default=default, height=height, width=width)

    def new_grid(self):
        """
        Initialize the Grid
        :return: New Grid
        """
        return np.zeros((self.height, self.width), dtype=np.int8)

    def get_grid(self):
        """
        :return: internal grid
        """
        return self.grid

    def get_grid_copy(self):
        return np.copy(self.grid)

    def copy(self):
        return ArrayBoard(grid=np.copy(self.get_grid()), height=copy.deepcopy(self.height), width=copy.deepcopy(self.width))

    def __copy__(self):
        return ArrayBoard(grid=self.get_grid(), height=self.height, width=self.width)

    def __deepcopy__(self, memo):
        return ArrayBoard(grid=np.copy(self.get_grid()), height=copy.deepcopy(self.height, memo), width=copy.deepcopy(self.width, memo))

    def set_grid(self, grid):
        """
        Set internal grid
        :param grid: internal grid
        """
        self.grid = grid

    def set_piece(self, position, piece):
        """
        :param position: Tuple (x, y) of position to place piece
        :param piece: piece to place
        """
        self.grid[abs(position[Y] - (self.height - 1))][position[X]] = piece

    def get_piece(self, position):
        """
        :param position: Tuple (x, y) of position to get
        :return: piece at position
        """
        return self.grid[abs(position[Y] - (self.height - 1))][position[X]]

    def __hash__(self):
        return tuple(self.grid.flatten())
