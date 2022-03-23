
def is_terminal(state):
    """
    Returns true if the current state is a terminal state.  By convention,
    a terminal state has zero future rewards.  Sometimes the terminal state(s)
    may have no possible actions.  It is also common to think of the terminal
    state as having a self-loop action 'pass' with zero reward; the formulations
    are equivalent.
     """
    return state.is_terminal()


class MDP:
    """
    A Markov Decision Process, defined by an initial state, transition model,
    and reward function. We also keep track of a gamma value, for use by
    algorithms. T(s, a) return a list of (p, s') pairs.
    We also keep track of the possible states, terminal states, and
    actions for each state.
    """

    def __init__(self, rewards):
        self.rewards = rewards
        self.living_reward = 0.0

    def set_living_reward(self, reward):
        """
        The (negative) reward for exiting "normal" states.

        This reward is on entering a state and therefore is not clearly part of the state's
        future rewards.
        """
        self.living_reward = reward

    def reward(self, state):
        """
        Return a numeric reward for this state. The reward depends on only the current state.
        """
        if state.get_current_player() == state.get_player2:  # neutralize board
            return self.rewards[-1 * state.get_board()]
        return self.rewards[state.get_board()]

    @staticmethod
    def transitions(state):
        """
        Transition model.  From a state and an action, return a list of (result-state, probability) pairs.
        """
        state = state
        actions = state.get_legal_actions()
        probability = 1 / len(actions)
        return list([(state.get_successor(action), probability) for action in actions])

    @staticmethod
    def actions(state):
        """
        Set of actions that can be performed in this state.  By default, a fixed list of actions,
        except for terminal states. Override this method if you need to specialize by state.
        """
        if state.is_terminal():
            return None
        return state.get_legal_actions()
