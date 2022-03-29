from abc import ABC
from collections import defaultdict
import random
import intelligence.learning_agent as learning
import intelligence.agent as agent
import intelligence.search_agents as sa
import game_components.connect_four as c4
import intelligence.successor_generator as gen
import os
import json
PLAYER2 = -1
WINNING_VALUE = 1000000
LOSING_VALUE = -1000000
TIE_VALUE = -10000


def reward_function(game, current_player):
    # Check for terminal state
    if game.get_status() == current_player:
        return (1 / (game.get_turn() + 1)) * WINNING_VALUE  # without the living penalty it trolls the opponent
    elif game.is_tie():
        return TIE_VALUE
    elif game.is_terminal_state():
        return (1 / (game.get_turn() + 1)) * LOSING_VALUE

    return 0.0


class Reinforcement(learning.Learning, ABC):
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
    def train(opponent, learning_rate: float = 1.0, exploration_rate: float = 0.05, discount_factor: float = 0.8,
              iterations: int = 10, reward_function=None):
        raise NotImplementedError


class QLearning(Reinforcement):
    """
    Q-Learning Agent
    """

    def __init__(self, values=None, learning_rate: float = 1.0, exploration_rate: float = 0.05, discount_factor: float = 0.8,
                 iterations: int = 10):
        """
        You can initialize Q-values here...
        """
        super().__init__(learning_rate, exploration_rate, discount_factor, iterations)
        if values is None:
            self.values = defaultdict(lambda: 0.0)
        else:
            self.values = values

    def get_q_value(self, state, action):
        """
        Returns Q(state,action), otherwise 0.0 if state has never been seen.
        """
        return self.values[hash(state) ^ hash(action)]

    def compute_value_from_q_values(self, state):
        """
        Returns max_action Q(state,action) over the legal actions.
        """
        if state.is_terminal_state():
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

        if state.is_terminal_state():
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
        if state.is_terminal_state():
            return None

        if random.random() < self.exploration_rate:
            action = random.choice(list(state.get_legal_actions()))
        else:
            action = self.get_policy(state)
        return action

    # def _neutralize_state(self, state):
    #     if self._player == PLAYER2:
    #         board, turn, status = state.get_state()
    #         grid = board.get_grid()
    #         grid *= -1
    #         board.set_grid(grid)
    #         state = c4.ConnectFour(state=(board, turn, status))
    #     return state

    def update(self, state, action, next_state, reward):
        """
        Called during transition observations, performs a Q-Value update.
        """

        sample = reward + self.discount_factor * self.compute_value_from_q_values(next_state)
        self.values[hash(state) ^ hash(action)] = (1.0 - self.learning_rate) * self.get_q_value(state,
                                                                                     action) + self.learning_rate * sample

    def get_policy(self, state):
        return self.compute_action_from_q_values(state)

    def get_value(self, state):
        return self.compute_value_from_q_values(state)

    @staticmethod
    def train(opponent, learning_rate: float = 1.0, exploration_rate: float = 0.05, discount_factor: float = 0.8,
              iterations: int = 10, reward_function=reward_function):
        """ todo
        :param opponent:
        :param learning_rate:
        :param exploration_rate:
        :param discount_factor:
        :param iterations:
        :param reward_function:
        :return: dictionary of parameters used, learned values
        """
        print("[Start Training]")

        learner = QLearning(None, learning_rate, exploration_rate, discount_factor, iterations)

        # todo - add progress bar and stats

        # Simulate Episodes
        while learner.is_training():
            print("Start Episode:", learner.current_iteration)
            learner.start_episode()

            # Initialize Game
            players = [learner, opponent]
            # random.shuffle(players)
            player1, player2 = players
            state = c4.ConnectFour()

            # Simulate Game
            print("\tSimulate Game")
            while not state.is_terminal_state():
                if state.get_current_player() == 1:
                    action = player1.get_action(state)
                else:
                    action = player2.get_action(state)

                next_state = gen.GENERATOR.get_successor(state, action)
                reward = reward_function(next_state, learner.get_player())

                learner.observe_transition(state, action, next_state, reward)

                state = next_state

            print(f"\tt={state.get_turn():03d}; s={state.get_status()}")
            learner.stop_episode()


        return learner.values


if __name__ == '__main__':
    values = QLearning.train(sa.AlphaBeta(depth_limit=1), iterations=1000, exploration_rate=.60, learning_rate=0.0001, discount_factor=.9)
    file = "./data/values.json"

    try:
        with open(file, "w") as write:
            json.dump(values, fp=write, sort_keys=True, indent=2)
            print("Save Successfully")

    except FileNotFoundError:
        print("File not Found.")

    except IOError:
        print("IO Error")



