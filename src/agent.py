from random import choice

POSITIVE_INF = float("inf")
NEGATIVE_INF = float("-inf")


# todo check this eval function
def evaluation_function_simple(game) -> int:
    turn, status = game.get_turn(), game.get_status()
    a = 0
    if status == game.get_current_player():
        a = POSITIVE_INF  # win
    elif game.is_terminal_state():
        a = NEGATIVE_INF  # loss or tie
    return a - 2 * turn  # negative living reward


def simple_depth_function_depth(game, depth_limit) -> int:
    return depth_limit


class Agent:
    """
    An agent must define a get_action method
    """

    def __init__(self, eval_function=evaluation_function_simple):
        self.__evaluation_function = eval_function

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
            utilities = [self.__evaluation_function(game.get_successor_game(move))
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

    def __init__(self, depth_limit=2, eval_fn=evaluation_function_simple, depth_fn=simple_depth_function_depth):
        super().__init__(eval_fn)
        self.__depth_limit = depth_limit
        self.__get_depth_limit = depth_fn


class MiniMax(MultiAgent):
    """
    A multi-agent which chooses an action at each choice point by attempting to maximize its utility and
    minimize the utility of its opponent.  Utility of a state is defined by an evaluation function.
    """

    def get_action(self, game_state):
        v, move = self.__max_value(game_state, 0)
        return move

    def __max_value(self, game_state, current_depth):
        if game_state.is_terminal_state() or self.__get_depth_limit(game_state, self.__depth_limit) <= current_depth:
            return self.__evaluation_function(game_state), None

        v, move = NEGATIVE_INF, None
        best_moves = []

        for a in game_state.get_legal_actions():
            v2, a2 = self.__min_value(game_state.get_successor_game(a), current_depth)
            if v2 == v:
                best_moves.append(a)
            if v2 > v:
                v, move = v2, a
                best_moves.clear()
                best_moves.append(a)
        if len(best_moves) != 0:
            move = choice(best_moves)

        return v, move

    def __min_value(self, game_state, current_depth):
        if game_state.is_terminal_state():
            return self.__evaluation_function(game_state), None

        v, move = POSITIVE_INF, None

        for a in game_state.get_legal_actions():
            v2, a2 = self.__max_value(game_state.get_successor_game(a), current_depth + 1)
            if v2 < v:
                v, move = v2, a
        return v, move
