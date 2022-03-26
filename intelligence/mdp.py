from game_components.game import PLAYER2

POSITIVE_INF = float("inf")
NEGATIVE_INF = float("-inf")
WINNING_VALUE = POSITIVE_INF
LOSING_VALUE = -999999
TIE_VALUE = -9999


class MDP:
    """
    A Markov Decision Process, defined by an initial state, transition model,
    and reward function. We also keep track of a gamma value, for use by
    algorithms. T(s, a) return a list of (p, s') pairs.
    We also keep track of the possible states, terminal states, and
    actions for each state.
    """

    def __init__(self):
        self.living_reward = 0.0

    def set_living_reward(self, reward):
        """
        The (negative) reward for exiting "normal" states.

        This reward is on entering a state and therefore is not clearly part of the state's
        future rewards.
        """
        self.living_reward = reward

    @staticmethod
    def get_possible_actions(state):
        """
        Set of actions that can be performed in this state.
        """
        if state.is_terminal():
            return None
        return state.get_legal_actions()

    def get_states(self):
        """
        Return list of all states.
        """
        # The true terminal state.
        states = [self.grid.terminal_state]
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                if self.grid[x][y] != '#':
                    state = (x, y)
                    states.append(state)
        return states

    def get_reward(self, state, current_player):
        """
        Return a numeric reward for this state. The reward depends on only the current state.
        """
        # Check for terminal state
        if state.get_status() == current_player:
            return WINNING_VALUE
        elif state.is_tie():
            return TIE_VALUE
        elif state.is_terminal_state():
            return LOSING_VALUE

        return 0.0

    @staticmethod
    def get_transitions(state):
        """
        Transition model.  From a state and an action, return a list of (result-state, probability) pairs.
        """
        state = state
        actions = state.get_legal_actions()
        probability = 1 / len(actions)
        return list([(state.get_successor(action), probability) for action in actions])

    @staticmethod
    def is_terminal(state):
        return state.is_terminal_state()
