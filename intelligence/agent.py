from intelligence.evaluation_fn_wtsq import evaluation_function_weighted_square as wtsq


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
        The Agent will receive a game and must return an action from the legal moves

        :param game: current state of the game
        :return: The action chosen by the agent given the game
        """
        self._player = game.get_current_player()
        self._opponent = -1 * self._player
        return self._get_action(game)

    def _get_action(self, game):
        raise NotImplementedError()
