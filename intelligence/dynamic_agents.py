from intelligence.agent import Agent


class Dynamic(Agent):

    def __init__(self, player, learning_rate=1.0, exploration_rate=0.05, discount=0.8, iterations=100):
        """
        :param player: current player
        :param learning_rate:
        :param exploration_rate:
        :param discount:
        :param iterations:
        """
        super().__init__(player)
        self.learning_rate = learning_rate
        self.exploration_rate = exploration_rate
        self.discount = discount
        self.iterations = iterations

    def get_action(self, state):
        pass

    def get_q_state(self, state, action):
        """
        Get state after transitioned with action
        :param state:
        :param action:
        :return:
        """
        pass

    def value_iteration(self, mdp, epsilon=0.001):
        """
        solve the mdp
        :param mdp:
        :param epsilon:
        :return:
        """
        pass

    def best_policy(self, mdp, utility_fn):
        """
        Given an MDP and a utility function U, determine the best policy,
        as a mapping from state to action.
        :param mdp:
        :param utility_fn:
        :return:
        """
        pass

    def best_value(self, mdp):
        pass

    def expected_utility(self, mdp, utility_fn, action, state):
        """
        The expected utility of doing action in state, according to the MDP and utility function.
        :param mdp:
        :param utility_fn:
        :param action:
        :param state:
        :return:
        """
        pass

    def policy_iteration(self, mdp):
        """
        Solve an MDP
        :param mdp:
        :return:
        """

    def policy_evaluation(self, mdp, utility_fn, _table, k=20):
        """
        Return an updated utility mapping utility function from each state in the MDP to its
        utility, using an approximation (modified policy iteration).
        :param mdp:
        :param utility_fn:
        :param pi_table:
        :param k:
        :return:
        """
