from abc import ABC
from collections import Counter
from intelligence.agent import Agent
from intelligence.learning_agent import Learning
import random
import game_components
from intelligence.successor_generator import GENERATOR
from tqdm import tqdm


class Reinforcement(Learning, ABC):
    """
    Reinforcement Agent: which estimates Q-Values (as well as policies) from experience rather than a model.
    """

    def __init__(self, learning_rate: float = 1.0, exploration_rate: float = 0.05, discount_factor: float = 0.8,
                 iterations: int = 10):
        super().__init__(learning_rate, exploration_rate, discount_factor, iterations)

        self.accum_train_rewards = 0.0
        self.accum_test_rewards = 0.0

        self.last_state = None
        self.last_action = None
        self.iteration_rewards = 0.0

    def observe_transition(self, state, action, next_state, delta_reward):
        """
        Called during training, calls the self.update method and informs agent that a transition has been observed.
        """
        self.iteration_rewards += delta_reward
        self.update(state, action, next_state, delta_reward)

    def start_episode(self):
        """
        Called during training, when new episode is starting
        """
        self.last_state = None
        self.last_action = None
        self.iteration_rewards = 0.0

    def stop_episode(self):
        """
        Called during training, when episode is done
        """
        if self.current_iteration < self.iterations:
            self.accum_train_rewards += self.iteration_rewards
        else:
            self.accum_test_rewards += self.iteration_rewards
        self.current_iteration += 1
        if self.current_iteration >= self.iterations:
            # Take off the training wheels
            self.exploration_rate = 0.0  # no exploration
            self.learning_rate = 0.0  # no learning

    def is_training(self):
        return self.current_iteration < self.iterations

    def is_testing(self):
        return not self.is_training()

    def update(self, state, action, next_state, reward):
        """
        will be called after observing a transition and reward
        """
        raise NotImplementedError

    def get_q_value(self, state, action):
        """
        Should return Q(state,action)
        """
        raise NotImplementedError

    def get_value(self, state):
        """
        What is the value of this state under the best action?
        Concretely, this is given by

        V(s) = max_{a in actions} Q(s,a)
        """
        raise NotImplementedError

    def get_policy(self, state):
        """
        What is the best action to take in the state. Note that because
        we might want to explore, this might not coincide with get_action
        Concretely, this is given by

        policy(s) = arg_max_{a in actions} Q(s,a)

        If many actions achieve the maximal Q-value,
        it doesn't matter which is selected.
        """
        raise NotImplementedError

    @staticmethod
    def train(learning_rate: float = 1.0, exploration_rate: float = 0.05, discount_factor: float = 0.8,
              iterations: int = 10, reward_function=None, opponent_swap_rate=0, *opponents):
        raise NotImplementedError


class QLearning(Reinforcement):
    """
    Q-Learning Agent
    """

    def __init__(self, values=None, *args):
        """
        You can initialize Q-values here...
        :param args:
        """
        super().__init__(*args)

        if values is None:
            self.values = Counter()
        else:
            self.values = values

    def get_q_value(self, state, action):
        """
        Returns Q(state,action), otherwise 0.0 if state has never been seen.
        """
        return self.values[(state, action)]

    def compute_value_from_q_values(self, state):
        """
        Returns max_action Q(state,action) over the legal actions.
        """
        if state.is_terminal():
            return 0.0

        value = float('-inf')

        for action in state.get_legal_actions():
            value = max(value, self.get_q_value(state, action))

        return value

    def compute_action_from_q_values(self, state):
        """
        Compute the best action to take in a state.
        """
        best_action = None

        if state.is_terminal():
            return None

        value = float('-inf')

        for action in state.get_legal_actions():
            q = self.get_q_value(state, action)
            if value < q:
                best_action = action
                value = q

        return best_action

    def _get_action(self, state, time_start):
        """
        Compute the action to take in the current state.
        With probability self.exploration_rate a random action is taken, otherwise take on-policy action.
        """
        if state.is_terminal():
            return None

        if random.random() < self.exploration_rate:
            action = random.choice(state.get_legal_actions())
        else:
            action = self.get_policy(state)
        return action

    def update(self, state, action, next_state, reward):
        """
        Called during transition observations, performs a Q-Value update.
        """

        sample = reward + self.discount_factor * self.compute_value_from_q_values(next_state)
        self.values[(state, action)] = (1.0 - self.learning_rate) * self.get_q_value(state,
                                                                                     action) + self.learning_rate * sample

    def get_policy(self, state):
        return self.compute_action_from_q_values(state)

    def get_value(self, state):
        return self.compute_value_from_q_values(state)

    @staticmethod
    def train(learning_rate: float = 1.0, exploration_rate: float = 0.05, discount_factor: float = 0.8,
              iterations: int = 10, reward_function=None, opponent_swap_rate=0, *opponents):
        learner = QLearning(learning_rate, exploration_rate, discount_factor, iterations)

        # todo - add progress bar and stats
        while learner.is_training():
            learner.start_episode()

            state = game_components.ConnectFour()  # initial state

            while state.is_active_state():
                # todo
                # Shuffle Players
                players = [learner, opponents]
                random.shuffle(players)
                player1, player2 = players

                if state.get_current_player() == 1:
                    action = player1.get_action(state)
                else:
                    action = player2.get_action(state)

                next_state = GENERATOR.get_successor(state, action)
                reward = reward_function(next_state)  # some reward function

                learner.observe_transition(state, action, next_state, reward)

            learner.stop_episode()

            # todo - return hyperparams and values data
