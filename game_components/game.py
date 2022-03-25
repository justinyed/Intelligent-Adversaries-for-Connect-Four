from game_components.board import BoardInterface

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
        get tuple containing the tuple of the state at the start of a game_components

        :return: tuple of the state at the start of a game_components
        """
        pass

    def _get_state(self) -> tuple:
        """
        get tuple containing the tuple of the current state of the game_components

        :return: the state of the game_components as a tuple
        """
        pass

    def get_successor(self, action) -> tuple:
        """
        get the game_components object after an action is performed on the current state

        :param action: that leads to returned game_components
        :return: game_components after the applied action
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
        get _status of the game_components is an integer code representing the _status.

        :return: _status of the game_components
        """
        return self._status

    def set_status(self, status: int) -> None:
        """
        set _status of the game_components is an integer code representing the _status.

        :param status: code (integer)
        """
        self._status = status

    def set_state(self, state):
        """
        set the state of the game_components
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
        boolean for if the game_components is in a terminal state.

        :return: True if terminal state has been reached, otherwise False.
        """
        pass

    def is_active_state(self) -> bool:
        """
        boolean for if the game_components is NOT in a terminal state.

        :return: True if terminal state has NOT been reached, otherwise False.
        """
        return not self.is_terminal_state()

    def is_tie(self) -> bool:
        """
        boolean for if the game_components is in a tied state.
        :return: True if tied status
        """
        return self.get_status() == self.get_tie_code()

    def perform_action(self, directive) -> int:
        """
        given a directive execute action/move upon the game_components state.

        :param directive: parameter for action specification
        :return: updated _status code of the game_components
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
