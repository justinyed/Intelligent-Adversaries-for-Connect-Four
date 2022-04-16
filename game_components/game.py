import game_components.board as board

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
        :param tie: tie code to use for games in tie status; default=TIE_CODE
        :param turn: starting turn; default=0
        :param status: starting status; default=0
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
        get code used for tie games

        :return: tie code
        """
        return self._tie

    def get_players(self) -> tuple:
        """
        get tuple of pLayers

        :return: tuple of players
        """
        return self._players

    def get_player_count(self) -> int:
        """
        get number of players

        :return: count of players as int
        """
        return self._player_count

    def get_current_player(self) -> int:
        """
        get the current player from the tuple of players

        :return: current player
        """
        pass

    def get_board(self) -> board.BoardInterface:
        """
        get internal board

        :return: internal board
        """
        return self._board

    def set_board(self, board):
        """
        set internal board

        :param board: to set
        """
        self._board = board

    def _new_state(self) -> tuple:
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

    def get_successor(self, action) -> tuple:
        """
        get the game_components object after an action is performed on the current state

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
        return self._status

    def set_status(self, status: int) -> None:
        """
        set status of the game is an integer code representing the status.

        :param status: code (integer)
        """
        self._status = status

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

    def is_won(self) -> bool:
        """
        boolean for if the game is in a tied state.
        :return: True if win status
        """
        return self.is_terminal_state() and not self.is_tie()

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
