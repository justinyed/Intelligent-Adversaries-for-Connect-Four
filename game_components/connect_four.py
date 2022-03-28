import game_components.board as board
import game_components.game as game


class ConnectFour(game.GameInterface):
    """
    Internal Representation of the Game.
    """

    def __init__(self, board_type=board.ArrayBoard, state=None):
        super().__init__(board_type)

        # Initialize State
        if state is None:
            self._board, self._turn, self._status = self._new_state()
        else:
            self._board, self._turn, self._status = state

        self._max_turns = self._board.get_size() - 1  # -1 since turns start at 0
        self._player1 = self._players[0]
        self._player2 = self._players[1]
        self._n_connect = game.N_CONNECT
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

    def get_state(self):
        return self._board.copy(), self._turn, self._status

    def set_state(self, state):
        self._board, self._turn, self._status = state

    def get_successor(self, action):
        original_state = self.get_state()
        self.perform_action(action)
        new_state = self.get_state()
        self.set_state(original_state)
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
        return ConnectFour(state=self.get_state())

    def __eq__(self, other):
        return self.__hash__() == hash(other)

    def __hash__(self):
        return hash(self._board)
