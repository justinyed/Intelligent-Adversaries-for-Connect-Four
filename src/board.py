HEIGHT = 6
WIDTH = 7


class BoardInterface:
    """The Internal Representation of a Grid Style Board."""

    def __init__(self, height=HEIGHT, width=WIDTH, default=0, grid=None):
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
        self.grid = grid

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

    def serialize(self):
        """
        serialize board to be stored

        :return: serialized board
        """
        return f"h={self.height}," \
               f"w={self.width}," \
               f"d={self.default}," \
               f"g={str(self.grid)}"

    def __hash__(self):
        return self.__str__()

    def __str__(self):
        return str(self.grid)


class TupleBoard(BoardInterface):
    """
    The Internal Representation of a Grid Style Board Game.
    """

    def __init__(self, height=HEIGHT, width=WIDTH):
        super().__init__(height=height, width=width)

    def new_grid(self):
        """
        Initialize the Grid
        :return: New Grid
        """
        return tuple((self.default for _ in range(self.width * self.height)))

    def get_grid(self):
        """
        :return: internal grid
        """
        return self.grid

    def get_grid_copy(self):
        return tuple((self.grid[i]
                      for i in range(self.height * self.width)))

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