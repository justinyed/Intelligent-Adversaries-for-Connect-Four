from src.board import BoardInterface, ArrayBoard

EMPTY = 0
PLAYER1 = 1
PLAYER2 = -1
TIE_CODE = 3
X = 0
Y = 1
N_CONNECT = 4


class GameInterface:
    """Game Interface"""

    def __init__(self, board_type, players=(PLAYER1, PLAYER2), tie=TIE_CODE, turn=0, status=0):
        """
        Constructor for Game

        :param players: tuple of _players; default=(PLAYER1, PLAYER2)
        :param tie: _tie code to use for games in _tie _status; default=TIE_CODE
        :param turn: starting _turn; default=0
        :param status: starting _status; default=0
        """
        self._board = None
        self._board_type = board_type
        self._players = players
        self._player_count = len(self._players)
        self._tie = tie
        self._turn = turn
        self._status = status

    def get_tie_code(self) -> int:
        """
        get code used for _tie games

        :return: _tie code
        """
        return self._tie

    def get_players(self) -> tuple:
        """
        get tuple of pLayers

        :return: tuple of _players
        """
        return self._players

    def get_player_count(self) -> int:
        """
        get number of _players

        :return: count of _players as int
        """
        return self._player_count

    def get_current_player(self) -> int:
        """
        get the current current_player from the tuple of _players

        :return: current current_player
        """
        pass

    def get_board(self) -> BoardInterface:
        """
        get internal _board

        :return: internal _board
        """
        return self._board

    def set_board(self, board):
        """
        set internal _board

        :param board: to set
        """
        self._board = board

    def _new_state(self) -> tuple:
        """
        get tuple containing the tuple of the state at the start of a game

        :return: tuple of the state at the start of a game
        """
        pass

    def _get_state(self) -> tuple:
        """
        get tuple containing the tuple of the current state of the game

        :return: the state of the game as a tuple
        """
        pass

    def get_successor(self, action) -> tuple:
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
        get _status of the game is an integer code representing the _status.

        :return: _status of the game
        """
        return self._status

    def _set_state(self, state):
        """
        set the state of the game
        :param state: State to set
        """
        pass

    def get_turn(self) -> int:
        """
        get the current _turn number

        :return: Current Turn
        """
        return self._turn

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

    def is_tie(self) -> bool:
        """
        boolean for if the game is in a tied state.
        :return: True if tied status
        """
        return self.get_status() == self.get_tie_code()

    def perform_action(self, directive) -> int:
        """
        given a directive execute action/move upon the game state.

        :param directive: parameter for action specification
        :return: updated _status code of the game
        """
        pass

    def copy(self):
        """
        creates a deep copy of the board
        :return: copy
        """
        pass

    def __hash__(self):
        return hash(self._board)


class ConnectFour(GameInterface):
    """
    Internal Representation of the Game.
    """

    def __init__(self, board_type=ArrayBoard, state=None):
        super().__init__(board_type)

        # Initialize State
        if state is None:
            self._board, self._turn, self._status = self._new_state()
        else:
            self._board, self._turn, self._status = state

        self._max_turns = self._board.get_size() - 1  # -1 since turns start at 0
        self._player1 = self._players[0]
        self._player2 = self._players[1]
        self._n_connect = N_CONNECT
        self._in_progress = self._board.get_default()

    # --- Game Methods ---

    def get_player1(self):
        return self._player1

    def get_player2(self):
        return self._player2

    def get_default(self):
        return self.get_board().get_default()

    def get_max_turns(self) -> int:
        return self._max_turns

    def get_legal_actions(self):
        """
        :return: a generator which contains the legal moves
        """
        return self._board.get_legal_actions()

    def _new_state(self):
        """
        :return: new _grid, new _turn counter, new _status
        """
        board = self._board_type()
        return board, 0, board.get_default()

    def _get_state(self):
        return self._board.copy(), self._turn, self._status

    def _set_state(self, state):
        self._board, self._turn, self._status = state

    def get_successor(self, action):
        original_state = self._get_state()
        self.perform_action(action)
        new_state = self._get_state()
        self._set_state(original_state)
        return ConnectFour(state=new_state)

    def get_current_player(self):
        if self.get_status() != self._in_progress:
            return self.get_status()
        return self.get_players()[self.get_turn() % self._player_count]

    def is_terminal_state(self) -> bool:
        return self._in_progress != self.get_status()

    def __update_status(self, set_position) -> None:
        if self._board.check_win(set_position, self.get_current_player()):
            self._status = self.get_players()[self.get_turn() % self._player_count]
        elif self.check_tie():
            self._status = self._tie
        else:
            self._status = self._in_progress

    def perform_action(self, directive):
        if self.is_terminal_state():
            raise ValueError("Game is in Terminal State, yet an action was attempted.")

        position = self._board.drop_piece(directive, self.get_current_player())
        self.__update_status(position)
        status = self.get_status()
        if status == self._board.get_default():
            self._turn += 1  # increment _turn, move was actually made
        return status

    def check_tie(self) -> bool:
        return self._max_turns == self._turn

    def copy(self):
        return ConnectFour(state=self._get_state())

    def __eq__(self, other):
        return self.__hash__() == hash(other)

    def __hash__(self):
        return hash(self._board)




