import copy
import numpy as np

X = 0
Y = 1


class BoardInterface:
    """The Internal Representation of a Grid Style Board."""

    HEIGHT = 6
    WIDTH = 7
    _DEFAULT = 0
    _N_CONNECT = 4

    def __init__(self, grid=None, lowest=None):
        """
        constructor for board object

        :param grid: if one wants to copy an existing board
        """

        if grid is None and lowest is None:
            self._grid = self.new_grid()
            self._lowest = list([0 for _ in range(self.get_width())])
        elif grid is not None and lowest is not None:
            self._grid = grid
            self._lowest = lowest
        else:
            raise ValueError("_lowest and _grid must be provided together")

    def get_height(self):
        return self.HEIGHT

    def get_width(self):
        return self.WIDTH

    def get_default(self):
        return self._DEFAULT

    def get_size(self):
        return self.get_width() * self.get_height()

    def get_lowest(self):
        return self._lowest

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
        return self._grid

    def get_grid_copy(self):
        """
        get copy of grid

        :return: deep copy internal grid
        """
        pass

    def set_grid(self, grid):
        """
        set internal grid

        :param grid:
        """
        self._grid = grid

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

        :param piece: piece to place
        :param column: column to drop piece
        :return: new status after action
        """
        position = column, self._lowest[column]
        if self.is_legal_position(position):
            self._lowest[column] += 1
            self.set_piece(position, piece)
            return position

    def reindex_lowest(self):
        for y in range(self.get_height()):
            for x in range(self.get_width()):
                if self.get_piece((x, y)) != self.get_default():
                    self._lowest[x] += 1

    def get_legal_actions(self):
        """
        :return: a generator which contains the legal moves
        """
        return (x for x in range(self.get_width()) if self.get_piece((x, self.get_height() - 1)) == self.get_default())

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
        return self.__count_line(origin, direction, current_piece) >= self._N_CONNECT

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
        return 0 <= position[X] < self.get_width() and 0 <= position[Y] < self.get_height()

    def __str__(self):
        return str(self._grid)

    def __hash__(self):
        return hash(self._grid)


class ArrayBoard(BoardInterface):
    """
    The Internal Representation of a Grid Style Board Game.
    """

    def new_grid(self):
        """
        Initialize the Grid
        :return: New Grid
        """
        return np.zeros((self.get_height(), self.get_width()), dtype=np.int8)

    def get_grid_copy(self):
        return np.copy(self._grid)

    def copy(self):
        return ArrayBoard(grid=self.get_grid_copy(), lowest=copy.deepcopy(self.get_lowest()))

    def set_piece(self, position, piece):
        """
        :param position: Tuple (x, y) of position to place piece
        :param piece: piece to place
        """
        self._grid[abs(position[Y] - (self.get_height() - 1))][position[X]] = piece

    def get_piece(self, position):
        """
        :param position: Tuple (x, y) of position to get
        :return: piece at position
        """
        return self._grid[abs(position[Y] - (self.get_height() - 1))][position[X]]

    def __hash__(self):
        return hash(self.get_grid_copy().tostring())

    def __eq__(self, other):
        return self.__hash__() == hash(other)

    def __copy__(self):
        return ArrayBoard(grid=self.get_grid_copy(), lowest=self.get_lowest())

    def __deepcopy__(self, memodict=None):
        if memodict is None:
            memodict = {}
        return self.__copy__()
