from random import choice

from intelligence.action_queue import reflex_action_queue
from intelligence.evaluation_functions import evaluation_function_weighted_square as wtsq
import time


class Agent:
    """
    An agent must define a get_action method
    """

    def __init__(self, eval_fn=wtsq):
        """
        Agent Interface

        :param eval_fn: evaluation function (returns the static value of a state)
        """
        self.evaluation_function = eval_fn
        self._player = None
        self._opponent = None

    def get_action(self, game):
        """
        The Agent will receive a game_components and must return an action from the legal moves

        :param game: current state of the game_components
        :return: The action chosen by the agent given the game_components
        """
        self._player = game.get_current_player()
        self._opponent = -1 * self._player
        return self._get_action(game, time.time())

    def _get_action(self, game, time_start):
        raise NotImplementedError()


class Random(Agent):
    """
    A random agent chooses an action at random.
    """

    def _get_action(self, game, time_start):
        if game.is_active_state():
            return choice(list(game.get_legal_actions()))
        return None


class Reflex(Agent):
    """
    A reflex agent chooses an action at each choice point by naively comparing
    its options via an evaluation function.
    """

    def _get_action(self, game, time_start):
        if game.is_terminal_state():
            return None
        return reflex_action_queue(game, self.evaluation_function, self._player).get_best_action()
