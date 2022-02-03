from random import choice

Positive_Inf = float("inf")
Negative_Inf = float("-inf")


# todo check this eval function
def simple_evaluation_function(game) -> int:
    turn, status = game.get_turn(), game.get_status()
    a = 0
    if status == game.get_current_player():
        a = Positive_Inf  # win
    elif game.is_terminal_state():
        a = Negative_Inf  # loss or tie
    return a - 2 * turn  # negative living reward


class Agent:
    """
    An agent must define a get_action method
    """

    def __init__(self, eval_function=simple_evaluation_function):
        self.evaluation_function = eval_function

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
    A reflex agent chooses an action at each choice point by comparing
    its alternatives via an evaluation function.
    """

    def get_action(self, game):
        if game.is_active_state():
            possible_moves = list(game.get_legal_actions())
            print(possible_moves)
            utilities = [self.evaluation_function(game.get_successor_game(move))
                         for move in possible_moves]

            best_utility = max(utilities)
            best_indices = [index for index in range(len(utilities))
                            if utilities[index] == best_utility]

            return possible_moves[choice(best_indices)]
        return None
