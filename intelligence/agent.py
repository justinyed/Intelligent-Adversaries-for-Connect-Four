class Agent:
    """
    An agent must define a get_action method
    """

    def __init__(self, player, eval_fn=None):
        """
        Agent Interface

        :param eval_fn: evaluation function (returns the static value of a state)
        """
        self.evaluation_function = eval_fn
        self.player = player
        self.opponent = -1 * player

    def get_action(self, game):
        """
        The Agent will receive a game and must return an action from the legal moves

        :param game: current state of the game
        :return: The action chosen by the agent given the game
        """
        return 0
