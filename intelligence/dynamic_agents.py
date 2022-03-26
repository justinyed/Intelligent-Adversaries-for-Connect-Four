from intelligence.agent import Agent
from intelligence.mdp import MDP
from collections import defaultdict


class Dynamic(Agent):

    def __init__(self, mdp: MDP, learning_rate=1.0, exploration_rate=0.05, discount=0.8, iterations=100):
        """
        A Dynamic Agent takes a Markov decision process on initialization and runs value iteration
        for a given number of iterations using the supplied discount factor.

        :param learning_rate:
        :param exploration_rate:
        :param discount:
        :param iterations:
        """
        super().__init__()
        self.mdp = mdp
        self.learning_rate = learning_rate
        self.exploration_rate = exploration_rate
        self.discount = discount
        self.iterations = iterations
        self.values = defaultdict(lambda: 0)

        states = mdp.get_states()

        for i in range(self.iterations):
            # Repeat...
            updated_values = self.values.copy()

            for state in states:
                if not self.mdp.is_terminal(state):
                    # get best q value
                    max_value = -float('inf')
                    actions = mdp.get_possible_actions(state)
                    for action in actions:
                        q_value = self.compute_q_value_from_values(state, action)
                        max_value = max(max_value, q_value)

                    updated_values[state] = max_value

            self.values = updated_values

    def get_value(self, state):
        """
        Return the value of the state (computed by value iteration).
        """
        return self.values[state]

    def compute_q_value_from_values(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        # *** YOUR CODE HERE ***

        #  Returns list of (next_state, prob) pairs
        transition_states_prob = self.mdp.get_transition_states_and_probs(state, action)

        Sum = 0.0
        for pair in transition_states_prob:
            next_state = pair[0]
            probability = pair[1]

            reward = self.mdp.get_reward(state, action, next_state)
            discount = self.discount
            next_value = self.get_value(next_state)

            Sum += probability * (reward + discount * next_value)

        return Sum
















    def _get_action(self, state):
        pass

    def get_q_state(self, state, action):
        """
        Get state after transitioned with action
        :param state:
        :param action:
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

    def compute_q_value_from_values(self, state, action):
        pass
