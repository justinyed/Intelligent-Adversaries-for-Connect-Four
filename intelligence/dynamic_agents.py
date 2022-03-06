from intelligence.agent import Agent


class Dynamic(Agent):

    def get_action(self, game):
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
