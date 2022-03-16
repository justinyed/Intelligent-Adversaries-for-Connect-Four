import os
import pickle
import time
from random import choice

from lru import LRU

from intelligence.action_queue import reflex_action_queue
from intelligence.agent import Agent
from intelligence.evaluation_fn_wtsq import evaluation_function_weighted_square as wtsq

POSITIVE_INF = float("inf")
NEGATIVE_INF = float("-inf")
CACHE_FILE = '../data/successor_cache.pkl'

if not os.path.isfile(CACHE_FILE):
    with open(CACHE_FILE, 'wb') as file:
        lru = LRU(10000)
        lru['first'] = 0
        pickle.dump(lru, file)  # Least Recently Used Cache


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
        if game.is_terminal_state():
            return None
        return reflex_action_queue(game, self.evaluation_function, self.player).get_best_action()


class MultiAgent(Agent):
    """
    An adversarial agent which chooses an action at each choice point by comparing
    its possible actions and the possible actions of its opponent via an evaluation function.
    """

    def __init__(self, player, eval_fn=wtsq, depth_limit=2, depth_fn=depth_function_simple):
        """
        :param depth_limit: depth limit on the MiniMax depth search
        :param eval_fn: evaluation function (returns the static value of a state)
        :param depth_fn: depth function (returns the current depth limit)
        """
        super().__init__(player, eval_fn)
        self.depth_limit = depth_limit
        self.get_depth_limit = depth_fn
        self.time_limit = None  # seconds
        self.start_time = None
        with open(CACHE_FILE, 'rb') as file:
            self._successor_cache = pickle.load(file)  # Least Recently Used Cache

    def timer_set(self, seconds: int) -> None:
        self.time_limit = seconds

    def _timer_start(self) -> None:
        if self.time_limit is not None:
            self.start_time = time.time()

    def _is_timer_elapsed(self) -> bool:
        """
        True if timer has elapsed; false otherwise
        :return: True if timer has elapsed; otherwise False
        """
        return self.time_limit <= time.time() - self.start_time if self.time_limit is not None else False

    def _is_depth_max(self, game, current_depth) -> bool:
        return current_depth >= self.get_depth_limit(game, self.depth_limit)

    def get_successor(self, state, action):
        h = state.get_board().hash_board(action)
        if h in self._successor_cache:
            return self._successor_cache[h]
        else:
            g = state.get_successor(action)
            self._successor_cache[h] = g  # todo may create problems without deep copy?
            return g

    def __del__(self):
        with open(CACHE_FILE, 'wb') as file:
            pickle.dump(self._successor_cache, file)  # Least Recently Used Cache
        del self._successor_cache


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
        if self._is_timer_elapsed() or game.is_terminal_state() or self._is_depth_max(game, current_depth):
            return self.evaluation_function(game, self.player), None

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
            return self.evaluation_function(game, self.player), None

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

    def get_action(self, game):
        self._timer_start()
        _, move = self._max_value(game, 0, NEGATIVE_INF, POSITIVE_INF)
        return move

    def _max_value(self, game, current_depth, alpha, beta):
        if self._is_timer_elapsed() or game.is_terminal_state() or self._is_depth_max(game, current_depth):
            return self.evaluation_function(game, self.player), None

        value, best_actions = NEGATIVE_INF, []
        ordered_actions = reflex_action_queue(game, self.evaluation_function, self.player).get_actions()

        for action in ordered_actions:
            value_prime, _ = self._min_value(self.get_successor(game, action), current_depth, alpha, beta)
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

    def _min_value(self, game, current_depth, alpha, beta):
        if game.is_terminal_state():
            return self.evaluation_function(game, self.player), None

        value, best_action = POSITIVE_INF, None
        ordered_actions = reversed(reflex_action_queue(game, self.evaluation_function, self.player).get_actions())

        for action in ordered_actions:
            value_prime, _ = self._max_value(self.get_successor(game, action), current_depth + 1, alpha, beta)
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
    todo fix doc string
    """

    def __init__(self, player, eval_fn=wtsq, depth_limit=3, depth_fn=depth_function_simple):
        super().__init__(player, eval_fn, depth_limit, depth_fn)
        self.best_known_moves = dict()
        self.absolute_depth_limit = depth_limit

    def get_action(self, game):
        self._timer_start()
        self.best_known_moves.clear()
        move = None

        if game.get_turn() == 0:
            return reflex_action_queue(game, self.evaluation_function, self.player).get_best_action()

        # iterative deepening
        for current_depth_limit in range(0, self.absolute_depth_limit + 1):
            self.depth_limit = current_depth_limit
            _, move = self._max_value(game, 0, NEGATIVE_INF, POSITIVE_INF)

        return move
