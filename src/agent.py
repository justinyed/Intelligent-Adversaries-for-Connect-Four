from random import choice
from utils.action_queue import ActionQueue
from utils.evaluation_function_wtsq import evaluation_function_weighted_square as wtsq


POSITIVE_INF = float("inf")
NEGATIVE_INF = float("-inf")


def evaluation_function_simple(game):
    """
    Evaluates the state of the game and returns the static value of being in that state.

    :param game: game state to evaluate
    :return: static value in current state
    """

    if game.get_status() == game.get_current_player():
        return POSITIVE_INF  # win
    elif game.is_terminal_state():
        return NEGATIVE_INF  # loss or tie
    return 0


def depth_function_simple(game, depth_limit) -> int:
    """
    Just Returns the Depth Limit

    :param game: unused, but here for API consistency
    :param depth_limit: defined depth limit
    :return: depth limit
    """
    return depth_limit


class Agent:
    """
    An agent must define a get_action method
    """

    def __init__(self, evaluation_fn=wtsq):
        """
        Agent Interface

        :param evaluation_fn: evaluation function (returns the static value of a state)
        """
        self.evaluation_function = evaluation_fn

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
            utilities = [self.evaluation_function(game.get_successor_game(move))
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

    def __init__(self, depth_limit=2, eval_fn=wtsq, depth_fn=depth_function_simple):
        """
        :param depth_limit: depth limit on the MiniMax depth search
        :param eval_fn: evaluation function (returns the static value of a state)
        :param depth_fn: depth function (returns the current depth limit)
        """
        super().__init__(eval_fn)
        self.depth_limit = depth_limit
        self.get_depth_limit = depth_fn


class MiniMax(MultiAgent):
    """
    A multi-agent which chooses an action at each choice point by attempting to maximize its utility and
    minimize the utility of its opponent. Utility of a state is defined by an evaluation function.
    """

    def get_action(self, game_state):
        _, move = self._max_value(game_state, 0)
        return move

    def _max_value(self, game_state, current_depth):
        if game_state.is_terminal_state() or current_depth >= self.get_depth_limit(game_state, self.depth_limit):
            return self.evaluation_function(game_state), None

        value = NEGATIVE_INF
        best_actions = []

        for action in game_state.get_legal_actions():
            value_prime, _ = self._min_value(game_state.get_successor_game(action), current_depth)
            if value_prime == value:
                best_actions.append(action)

            if value_prime > value:
                value = value_prime
                best_actions.clear()
                best_actions.append(action)

        return value, choice(best_actions)

    def _min_value(self, game_state, current_depth):
        if game_state.is_terminal_state():
            return self.evaluation_function(game_state), None

        value, best_action = POSITIVE_INF, None

        for action in game_state.get_legal_actions():
            value_prime, _ = self._max_value(game_state.get_successor_game(action), current_depth + 1)
            if value_prime < value:
                value, best_action = value_prime, action
        return value, best_action


class AlphaBeta(MultiAgent):
    """
    A multi-agent which chooses an action at each choice point by attempting to maximize its utility and
    minimize the utility of its opponent.  Utility of a state is defined by an evaluation function.
    Additionally, this agent will focus on evaluating relevant states by pruning sub-trees with too few utility points.
    """

    def get_action(self, game_state):
        _, move = self._max_value(game_state, 0, NEGATIVE_INF, POSITIVE_INF)
        return move

    def _max_value(self, game_state, current_depth, alpha, beta):
        if game_state.is_terminal_state() or self.get_depth_limit(game_state, self.depth_limit) <= current_depth:
            return self.evaluation_function(game_state), None

        value, best_action = NEGATIVE_INF, None
        best_moves = []

        for action in game_state.get_legal_actions():
            value_prime, _ = self._min_value(game_state.get_successor_game(action), current_depth, alpha, beta)
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
            return self.evaluation_function(game_state), None

        value, best_action = POSITIVE_INF, None

        for action in game_state.get_legal_actions():
            value_prime, _ = self._max_value(game_state.get_successor_game(action), current_depth + 1, alpha, beta)
            if value_prime < value:
                value, best_action = value_prime, action
                beta = min(beta, value)
            if value < alpha:
                break
        return value, best_action


class IterativeDeepening(AlphaBeta):
    """
    todo WIP
    A multi-agent which chooses an action at each choice point by attempting to maximize its utility and
    minimize the utility of its opponent.  Utility of a state is defined by an evaluation function.
    Additionally, this agent will focus on evaluating relevant states by pruning sub-trees with too few utility points.
    """

    def __init__(self, depth_limit=3, eval_fn=evaluation_function_simple, depth_fn=depth_function_simple):
        super().__init__(depth_limit, eval_fn, depth_fn)
        self.best_known_moves = dict()
        self.iterative_depth_limit = 0
        self.current_depth_limit = 0

    def get_action(self, game_state):
        move = None
        # iterative deepening
        for current_depth_limit in range(0, self.depth_limit + 1):
            self.iterative_depth_limit = current_depth_limit
            self.best_known_moves[current_depth_limit] = ActionQueue(game_state.get_legal_actions())
            _, move = self._max_value(game_state, 0, NEGATIVE_INF, POSITIVE_INF)
        return move

    def _max_value(self, game_state, current_depth, alpha, beta):
        if game_state.is_terminal_state() or \
                self.get_depth_limit(game_state, self.iterative_depth_limit) <= current_depth:
            return self.evaluation_function(game_state), None

        value, best_action = NEGATIVE_INF, None
        best_moves = []

        for action in self.best_known_moves[current_depth]:
            value_prime, _ = AlphaBeta._min_value(self, game_state.get_successor_game(action), current_depth, alpha,
                                                  beta)
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
