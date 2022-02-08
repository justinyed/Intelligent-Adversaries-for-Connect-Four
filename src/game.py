from board import BoardInterface, TupleBoard

PLAYER1 = 1
PLAYER2 = -1
TIE_CODE = 3
N_CONNECT = 4


class GameInterface:
    """Game Interface"""

    def __init__(self, board_type, players=(PLAYER1, PLAYER2), tie=TIE_CODE, turn=0, status=0):
        """
        Constructor for Game

        :param players: tuple of players; default=(PLAYER1, PLAYER2)
        :param tie: tie code to use for games in tie status; default=TIE_CODE
        :param turn: starting turn; default=0
        :param status: starting status; default=0
        """
        self.board = None
        self.board_type = board_type
        self.players = players
        self.player_count = len(self.players)
        self.tie = tie
        self.turn = turn
        self.status = status

    def get_tie_code(self) -> int:
        """
        get code used for tie games

        :return: tie code
        """
        return self.tie

    def get_players(self) -> tuple:
        """
        get tuple of pLayers

        :return: tuple of players
        """
        return self.players

    def get_player_count(self) -> int:
        """
        get number of players

        :return: count of players as int
        """
        return self.player_count

    def get_current_player(self) -> int:
        """
        get the current player from the tuple of players

        :return: current player
        """
        pass

    def get_board(self) -> BoardInterface:
        """
        get internal board

        :return: internal board
        """
        return self.board

    def set_board(self, board):
        """
        set internal board

        :param board: to set
        """
        self.board = board

    def new_state(self) -> tuple:
        """
        get tuple containing the tuple of the state at the start of a game

        :return: tuple of the state at the start of a game
        """
        pass

    def get_state(self) -> tuple:
        """
        get tuple containing the tuple of the current state of the game

        :return: the state of the game as a tuple
        """
        pass

    def get_successor_state(self, action) -> tuple:
        """
        get the state after an action is performed on the current state

        :param action: action that leads to returned state
        :return: state after the applied action
        """
        pass

    def get_successor_game(self, action) -> tuple:
        """
        get the game object after an action is performed on the current state

        :param action: that leads to returned game
        :return: game after the applied action
        """
        pass

    def get_legal_actions(self) -> tuple:
        """
        get tuple of legal actions

        :return: tuple of legal actions
        """
        pass

    def get_status(self) -> int:
        """
        get status of the game is an integer code representing the status.

        :return: status of the game
        """
        return self.status

    def set_state(self, state):
        """
        set the state of the game
        :param state: State to set
        """
        pass

    def get_turn(self) -> int:
        """
        get the current turn number

        :return: Current Turn
        """
        return self.turn

    def is_terminal_state(self) -> bool:
        """
        boolean for if the game is in a terminal state.

        :return: True if terminal state has been reached, otherwise False.
        """
        pass

    def is_active_state(self) -> bool:
        """
        boolean for if the game is NOT in a terminal state.

        :return: True if terminal state has NOT been reached, otherwise False.
        """
        return not self.is_terminal_state()

    def perform_action(self, directive) -> int:
        """
        given a directive execute action/move upon the game state.

        :param directive: parameter for action specification
        :return: updated status code of the game
        """
        pass


class ConnectFour(GameInterface):
    """
    Internal Representation of the Game.
    """

    def __init__(self, board_type=TupleBoard, state=None):
        super().__init__(board_type)

        # Initialize State
        if state is None:
            self.board, self.turn, self.status = self.new_state()
        else:
            self.board, self.turn, self.status = state

        self.max_turns = self.board.width * self.board.height - 1  # -1 since turns start at 0
        self.player1 = self.players[0]
        self.player2 = self.players[1]
        self.n_connect = N_CONNECT
        self.in_progress = self.board.default

    # --- Game Methods ---

    def get_legal_actions(self):
        """
        :return: a generator which contains the legal moves
        """
        return (x for x in range(self.board.width) if
                self.board.get_piece((x, self.board.height - 1)) == self.board.default)

    def new_state(self):
        """
        :return: new grid, new turn counter, new status
        """
        board = self.board_type()
        return board, 0, board.default

    def get_state(self):
        return self.board.copy(), self.turn, self.status

    def set_state(self, state):
        self.board, self.turn, self.status = state

    def get_successor_state(self, action):
        original_state = self.get_state()
        self.drop_piece(action)
        new_state = self.get_state()

        self.set_state(original_state)
        return new_state

    def get_successor_game(self, action):
        return ConnectFour(state=self.get_successor_state(action))

    def get_current_player(self):
        if self.get_status() != self.in_progress:
            return self.get_status()
        return self.get_players()[self.get_turn() % self.player_count]

    def is_terminal_state(self):
        return self.in_progress != self.get_status()

    def perform_action(self, directive):
        return self.drop_piece(directive)

    def drop_piece(self, column):
        """
        drop piece into slot in grid

        :param column: column to drop piece
        :return: new status after action
        """
        if self.status != self.in_progress:
            return self.status
        for y in range(self.board.height):
            position = (column, y)
            if self.board.get_piece(position) == self.board.default:
                self.board.set_piece(position, self.get_current_player())
                self.__update_status(position)  # update status
                self.turn += 1  # increment turn, move was actually made
                return self.status

    def __update_status(self, set_position) -> None:
        if self.__check_tie():
            self.status = self.tie
        elif self.__check_for_win_local(set_position):
            self.status = 1 + (self.turn % self.player_count)
        else:
            self.status = self.in_progress

    def __check_tie(self):
        return self.max_turns == self.turn

    def __check_for_win_local(self, drop_position):
        """
        Local Win Check. Checks Starting from the dropped piece (change on grid)
        :param drop_position: Position of Dropped Piece
        :return: True if Win was found, otherwise False
        """
        return self.__check_line(drop_position, (0, 1)) or \
               self.__check_line(drop_position, (1, 0)) or \
               self.__check_line(drop_position, (1, 1)) or \
               self.__check_line(drop_position, (-1, 1))

    def __check_line(self, origin, direction):
        return self.__count_line(origin, direction) == self.n_connect

    def __count_line(self, origin, direction):
        x0, y0 = origin
        dx, dy = direction
        ndx, ndy = -1 * dx, -1 * dy
        count = 1

        while True:
            tx, ty = x0 + ndx, y0 + ndy
            transition = (tx, ty)
            if self.__is_legal_position(transition) and self.__is_same_as_current(transition):
                x0, y0 = transition
            else:
                break

        while True:
            tx, ty = x0 + dx, y0 + dy
            transition = (tx, ty)
            if self.__is_legal_position(transition) and self.__is_same_as_current(transition):
                x0, y0 = transition
                count += 1
            else:
                break
        return count

    def __is_legal_position(self, position):
        return 0 <= position[0] < self.board.width and 0 <= position[1] < self.board.height

    def __is_same_as_current(self, position):
        return self.get_current_player() == self.board.get_piece(position)
