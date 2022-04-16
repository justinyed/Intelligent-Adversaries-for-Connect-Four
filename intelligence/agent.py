import random
from random import choice
import time
import intelligence.action_queue
import intelligence.evaluation_functions
import intelligence.successor_generator as gen


class Agent:
    """
    An agent must define a get_action method
    """

    def __init__(self, eval_fn=intelligence.evaluation_functions.evaluation_function_weighted_matrix, get_successor=gen.GENERATOR.get_successor):
        """
        Agent Interface
        :param eval_fn: evaluation function (returns the static value of a state)
        """
        self.evaluation_function = eval_fn
        self._player = None
        self._opponent = None
        self.get_successor = get_successor

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

    def get_player(self):
        return self._player


class Random(Agent):
    """A random agent chooses an action at random."""

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
        return intelligence.action_queue.reflex_action_queue(game, self.evaluation_function, self._player).get_best_action()


class Insane(Agent):
    """
    Chooses the same move every time
    """

    def __init__(self, move):
        super().__init__()
        self.possible_actions = [0, 1, 2, 3, 4, 5, 6]
        self.move = random.choice(self.possible_actions)

    def _get_action(self, game, time_start):
        if game.is_terminal_state():
            return None
        if self.move in list(game.get_legal_actions()):
            return self.move
        else:
            return random.choice(list(game.get_legal_actions()))

