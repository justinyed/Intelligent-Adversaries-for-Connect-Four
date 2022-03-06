from random import choice
from functools import lru_cache
from lru import LRUCache as Lru
import pickle
import os


class MDP:
    """
    A Markov Decision Process, defined by an initial state, transition model,
    and reward function. We also keep track of a gamma value, for use by
    algorithms. T(s, a) return a list of (p, s') pairs.
    We also keep track of the possible states, terminal states, and
    actions for each state.
    """

    def __init__(self, initial_state, transition_model, reward_function):
        self.initial_state = initial_state
        self.transition_fn = transition_model
        self.reward_fn = reward_function

    def reward(self, state):
        """
        Return a numeric reward for this state.
        """
        pass

    def transition(self, state, action):
        """
        Transition model.  From a state and an action, return a list of (result-state, probability) pairs.
        """
        pass

    def actions(self, state):
        """
        Set of actions that can be performed in this state.  By default, a fixed list of actions,
        except for terminal states. Override this method if you need to specialize by state.
        """
        pass
