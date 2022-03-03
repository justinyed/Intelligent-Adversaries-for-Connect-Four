from random import choice
from utils.action_queue import ActionQueue
from utils.evaluation_function_wtsq import evaluation_function_weighted_square as wtsq
import time

POSITIVE_INF = float("inf")
NEGATIVE_INF = float("-inf")


def evaluation_function_simple(game, current_player):
    """
    Evaluates the state of the game and returns the static value of being in that state.

    :param current_player:
    :param game: game state to evaluate
    :return: static value in current state
    """

    if game.get_status() == current_player:
        return POSITIVE_INF  # win
    elif game.is_terminal_state():
        return NEGATIVE_INF  # loss or _tie
    return 0


def depth_function_simple(game, depth_limit) -> int:
    """
    Just Returns the Depth Limit

    :param game: unused, but here for API consistency
    :param depth_limit: defined depth limit
    :return: depth limit
    """
    return depth_limit


def depth_function_turn_bonus(game, depth_limit) -> int:
    """
    Returns the Depth Limit plus a bonus which is related to the games maturity

    :param game:
    :param depth_limit: defined depth limit
    :return: depth limit
    """
    turn = game.get_turn()

    if turn >= 15:
        return depth_limit + 1
    elif turn >= 22:
        return depth_limit + 2
    elif turn >= 30:
        return depth_limit + 3
    else:
        return depth_limit


class Agent:
    """
    An agent must define a get_action method
    """

    def __init__(self, evaluation_fn=wtsq, player=0):
        """
        Agent Interface

        :param evaluation_fn: evaluation function (returns the static value of a state)
        """
        self.evaluation_function = evaluation_fn
        self.player = player
        self.opponent = -1 * player

    def get_action(self, game):
        """
        The Agent will receive a game and must return an action from the legal moves

        :param game: current state of the game
        :return: The action chosen by the agent given the game
        """
        return 0


class Random(Agent):
    """
    A random agent chooses an action at random.
    """

    def get_action(self, game):
        if game.is_active_state():
            return choice(list(game.get_legal_actions()))
        return None


class Reflex(Agent):
    """
    A reflex agent chooses an action at each choice point by naively comparing
    its alternatives via an evaluation function.
    """

    def get_action(self, game):
        if game.is_active_state():
            possible_moves = list(game.get_legal_actions())
            utilities = [self.evaluation_function(game.get_successor_game(move), self.player)
                         for move in possible_moves]

            best_utility = max(utilities)
            best_indices = [index for index in range(len(utilities))
                            if utilities[index] == best_utility]

            return possible_moves[choice(best_indices)]
        return None


class MultiAgent(Agent):
    """
    An adversarial agent which chooses an action at each choice point by comparing
    its possible actions and the possible actions of its opponent via an evaluation function.
    """

    def __init__(self, depth_limit=2, eval_fn=wtsq, depth_fn=depth_function_simple, player=0):
        """
        :param depth_limit: depth limit on the MiniMax depth search
        :param eval_fn: evaluation function (returns the static value of a state)
        :param depth_fn: depth function (returns the current depth limit)
        """
        super().__init__(eval_fn, player)
        self.depth_limit = depth_limit
        self.get_depth_limit = depth_fn
        self.time_limit = None  # seconds
        self.start_time = None

    def timer_set(self, seconds: int) -> None:
        self.time_limit = seconds

    def _timer_start(self) -> None:
        if self.time_limit is not None:
            self.start_time = time.time()

    def _timer_elapsed(self) -> bool:
        """
        True if timer has elapsed; false otherwise
        :return: True if timer has elapsed; otherwise False
        """
        return self.time_limit <= time.time() - self.start_time if self.time_limit is not None else False


class MiniMax(MultiAgent):
    """
    A multi-agent which chooses an action at each choice point by attempting to maximize its utility and
    minimize the utility of its opponent. Utility of a state is defined by an evaluation function.
    """

    def get_action(self, game):
        self._timer_start()
        _, move = self._max_value(game, 0)
        return move

    def _max_value(self, game, current_depth):
        if self._timer_elapsed() or game.is_terminal_state() or current_depth >= self.get_depth_limit(game,
                                                                                                      self.depth_limit):
            return self.evaluation_function(game, self.player), None

        value, best_actions = NEGATIVE_INF, []

        for action in game.get_legal_actions():
            value_prime, _ = self._min_value(game.get_successor_game(action), current_depth)
            if value_prime == value:
                best_actions.append(action)

            if value_prime > value:
                value = value_prime
                best_actions.clear()
                best_actions.append(action)

        return value, choice(best_actions)

    def _min_value(self, game, current_depth):
        if game.is_terminal_state():
            return self.evaluation_function(game, self.player), None

        value, best_action = POSITIVE_INF, None

        for action in game.get_legal_actions():
            value_prime, _ = self._max_value(game.get_successor_game(action), current_depth + 1)
            if value_prime < value:
                value, best_action = value_prime, action
        return value, best_action


class AlphaBeta(MultiAgent):
    """
    A multi-agent which chooses an action at each choice point by attempting to maximize its utility and
    minimize the utility of its opponent.  Utility of a state is defined by an evaluation function.
    Additionally, this agent will focus on evaluating relevant states by pruning subtrees with too few utility points.
    """

    def get_action(self, game):
        self._timer_start()
        _, move = self._max_value(game, 0, NEGATIVE_INF, POSITIVE_INF)
        return move

    def _max_value(self, game, current_depth, alpha, beta):
        if self._timer_elapsed() or game.is_terminal_state() or \
                self.get_depth_limit(game, self.depth_limit) <= current_depth:
            return self.evaluation_function(game, self.player), None

        value, best_action = NEGATIVE_INF, None
        best_moves = []

        for action in game.get_legal_actions():
            value_prime, _ = self._min_value(game.get_successor_game(action), current_depth, alpha, beta)
            if value_prime == value:
                best_moves.append(action)
            if value_prime > value:
                value = value_prime
                alpha = max(alpha, value)
                best_moves.clear()
                best_moves.append(action)
            if value > beta:
                break
        return value, choice(best_moves)

    def _min_value(self, game_state, current_depth, alpha, beta):
        if game_state.is_terminal_state():
            return self.evaluation_function(game_state, self.player), None

        value, best_action = POSITIVE_INF, None

        for action in game_state.get_legal_actions():
            value_prime, _ = self._max_value(game_state.get_successor_game(action), current_depth + 1, alpha, beta)
            if value_prime < value:
                value, best_action = value_prime, action
                beta = min(beta, value)
            if value < alpha:
                break
        return value, best_action


class IterativeDeepening(MultiAgent):
    """
    A multi-agent which chooses an action at each choice point by attempting to maximize its utility and
    minimize the utility of its opponent.  Utility of a state is defined by an evaluation function.
    Additionally, this agent will focus on evaluating relevant states by pruning subtrees with too few utility points.
    todo fix doc string
    """

    def __init__(self, depth_limit=3, eval_fn=wtsq, depth_fn=depth_function_simple, player=0):
        super().__init__(depth_limit, eval_fn, depth_fn, player)
        self.best_known_moves = dict()
        self.iterative_depth_limit = 0
        self.current_depth_limit = 0

    def get_action(self, game):
        self._timer_start()
        ordered_initial_queue = ActionQueue.build_naive_action_queue(game, self.evaluation_function, self.player)
        move = ordered_initial_queue.get_best()
        if game.get_turn() == 0:
            return move

        # iterative deepening
        for current_depth_limit in range(0, self.depth_limit + 1):
            self.iterative_depth_limit = current_depth_limit
            self.best_known_moves[current_depth_limit] = ordered_initial_queue.copy()
            _, move = self._max_value(game, 0, NEGATIVE_INF, POSITIVE_INF)
        return move

    def _max_value(self, game_state, current_depth, alpha, beta):
        # todo handle when time has elapsed
        if self._timer_elapsed() or game_state.is_terminal_state() or \
                self.get_depth_limit(game_state, self.iterative_depth_limit) <= current_depth:
            return self.evaluation_function(game_state, self.player), None

        value, best_action = NEGATIVE_INF, None
        best_moves = []

        for _, action in self.best_known_moves[current_depth]:
            value_prime, _ = self._min_value(game_state.get_successor_game(action), current_depth, alpha, beta)
            if value_prime == value:
                self.best_known_moves[current_depth].append((value, action))
            if value_prime > value:
                value = value_prime
                alpha = max(alpha, value)
                best_moves.clear()
                best_moves.append(action)
            if value > beta:
                break
        self.best_known_moves[current_depth].extend(best_moves)
        return value, choice(best_moves)

    def _min_value(self, game_state, current_depth, alpha, beta):
        if game_state.is_terminal_state():
            return self.evaluation_function(game_state, self.player), None

        value, best_action = POSITIVE_INF, None

        for action in game_state.get_legal_actions():
            value_prime, _ = self._max_value(game_state.get_successor_game(action), current_depth + 1, alpha, beta)
            if value_prime < value:
                value, best_action = value_prime, action
                beta = min(beta, value)
            if value < alpha:
                break
        return value, best_action
