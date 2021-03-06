import time
from abc import ABC
from random import choice
import intelligence.agent
import intelligence.action_queue
import intelligence.evaluation_functions

POSITIVE_INF = float("inf")
NEGATIVE_INF = float("-inf")
from lru import LRU


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


class MultiAgent(intelligence.agent.Agent, ABC):
    """
    An adversarial agent which chooses an action at each choice point by comparing
    its possible actions and the possible actions of its opponent via an evaluation function.
    """

    def __init__(self, eval_fn=intelligence.evaluation_functions.evaluation_function_weighted_matrix, depth_limit=2,
                 depth_fn=depth_function_simple):
        """
        :param depth_limit: depth limit on the MiniMax depth search
        :param eval_fn: evaluation function (returns the static value of a state)
        :param depth_fn: depth function (returns the current depth limit)
        """
        super().__init__(eval_fn)
        self.depth_limit = depth_limit
        self.get_depth_limit = depth_fn
        self.time_limit = None  # seconds

    def timer_set(self, seconds: int) -> None:
        self.time_limit = seconds

    @staticmethod
    def is_timer_elapsed(time_limit, time_start) -> bool:
        """
        True if timer has elapsed; false otherwise
        :return: True if timer has elapsed; otherwise False
        """
        return time_limit <= time.time() - time_start \
            if time_limit is not None else False

    def _is_depth_max(self, game, current_depth) -> bool:
        return current_depth >= self.get_depth_limit(game, self.depth_limit)


class MiniMax(MultiAgent):
    """
    A multi-agent which chooses an action at each choice point by attempting to maximize its utility and
    minimize the utility of its opponent. Utility of a state is defined by an evaluation function.
    """

    def _get_action(self, game, time_start):
        self.looks = 0
        if game.get_turn() == 0:
            return intelligence.action_queue.reflex_action_queue(game, self.evaluation_function,
                                                                 self._player).get_best_action()

        _, move = self._max_value(game, 0)
        return move

    def _max_value(self, game, current_depth):
        if game.is_terminal_state() or self._is_depth_max(game, current_depth):
            return self.evaluation_function(game, self._player), None

        value, best_actions = NEGATIVE_INF, []

        for action in game.get_legal_actions():
            value_prime, _ = self._min_value(self.get_successor(game, action), current_depth)
            if value_prime == value:
                best_actions.append(action)

            if value_prime > value:
                value = value_prime
                best_actions.clear()
                best_actions.append(action)

        return value, choice(best_actions)

    def _min_value(self, game, current_depth):
        if game.is_terminal_state():
            return self.evaluation_function(game, self._player), None

        value, best_action = POSITIVE_INF, None

        for action in game.get_legal_actions():
            value_prime, _ = self._max_value(self.get_successor(game, action), current_depth + 1)
            if value_prime < value:
                value, best_action = value_prime, action
        return value, best_action


class AlphaBeta(MultiAgent):
    """
    A multi-agent which chooses an action at each choice point by attempting to maximize its utility and
    minimize the utility of its opponent.  Utility of a state is defined by an evaluation function.
    Additionally, this agent will focus on evaluating relevant states by pruning subtrees with too few utility points.
    """

    def _get_action(self, game, time_start):

        if game.get_turn() == 0:
            return intelligence.action_queue.reflex_action_queue(game, self.evaluation_function,
                                                                 self._player).get_best_action()

        _, move = self._max_value(game, 0, NEGATIVE_INF, POSITIVE_INF, time_start)
        return move

    def _max_value(self, game, current_depth, alpha, beta, time_start):
        if MultiAgent.is_timer_elapsed(self.time_limit, time_start) \
                or game.is_terminal_state() \
                or self._is_depth_max(game, current_depth):
            return self.evaluation_function(game, self._player), None

        value, best_actions = NEGATIVE_INF, []
        ordered_actions = intelligence.action_queue.reflex_action_queue(game, self.evaluation_function,
                                                                        self._player).get_actions()

        for action in ordered_actions:
            value_prime, _ = self._min_value(self.get_successor(game, action),
                                             current_depth, alpha, beta, time_start)
            if value_prime == value:
                best_actions.append(action)
            if value_prime > value:
                value = value_prime
                alpha = max(alpha, value)
                best_actions.clear()
                best_actions.append(action)
            if value > beta:
                break
        return value, choice(best_actions)

    def _min_value(self, game, current_depth, alpha, beta, time_start):
        if game.is_terminal_state():
            return self.evaluation_function(game, self._player), None

        value, best_action = POSITIVE_INF, None
        ordered_actions = reversed(
            intelligence.action_queue.reflex_action_queue(game, self.evaluation_function, self._player).get_actions())

        for action in ordered_actions:
            value_prime, _ = self._max_value(self.get_successor(game, action),
                                             current_depth + 1, alpha, beta, time_start)
            if value_prime < value:
                value, best_action = value_prime, action
                beta = min(beta, value)
            if value < alpha:
                break
        return value, best_action


class IterativeDeepening(AlphaBeta):
    """
    A multi-agent which chooses an action at each choice point by attempting to maximize its utility and
    minimize the utility of its opponent.  Utility of a state is defined by an evaluation function.
    Additionally, this agent will focus on evaluating relevant states by pruning subtrees with too few utility points.
    """

    def __init__(self, eval_fn=intelligence.evaluation_functions.evaluation_function_weighted_matrix, depth_limit=3,
                 depth_fn=depth_function_simple, time_limit=5.0):
        super().__init__(eval_fn, depth_limit, depth_fn)
        self.absolute_depth_limit = depth_limit
        self.time_limit = time_limit
        self._cache = LRU(100000)

    def get_action(self, game):
        """
        The Agent will receive a game_components and must return an action from the legal moves
        :param game: current state of the game_components
        :return: The action chosen by the agent given the game_components
        """

        h = hash(game)

        if h in self._cache:
            return self._cache[h]
        else:  # store
            self._player = game.get_current_player()
            self._opponent = -1 * self._player
            a = self._get_action(game, time.time())
            self._cache[h] = a
            return a

    def _get_action(self, game, time_start):

        if game.get_turn() == 0:
            return intelligence.action_queue.reflex_action_queue(game, self.evaluation_function,
                                                                 self._player).get_best_action()

        moves = []

        # iterative deepening
        for current_depth_limit in range(1, self.absolute_depth_limit + 1):
            self.depth_limit = current_depth_limit
            _, move = self._max_value(game, 0, NEGATIVE_INF, POSITIVE_INF, time_start)
            if MultiAgent.is_timer_elapsed(self.time_limit, time_start):
                break
            else:
                moves.append(move)
        return moves[-1]
