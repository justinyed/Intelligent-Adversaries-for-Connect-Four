from intelligence.dynamic_agents import Dynamic


class Learning(Dynamic):

    def __init__(self, player, learning_rate=1.0, exploration_rate=0.05, discount=0.8, num_training=10):
        """

        :param player:
        :param learning_rate:
        :param exploration_rate:
        :param discount:
        :param num_training: number of training episodes (no learning after these many episodes).
        """
        super().__init__(player, learning_rate, exploration_rate, discount, num_training)
        self.num_episodes_completed = 0
        self.accum_train_rewards = 0.0
        self.accum_test_rewards = 0.0
        self.episode_rewards = 0.0

    def get_action(self, state):
        pass

    def update(self, state, action, next_state, reward):
        """
        Update Observation for transition and reward.
        """
        pass

    def observe_transition(self, state, action, next_state, delta_reward):
        """
        Called by environment to inform agent that a transition has been observed.
        This will update observations on the same arguments
        """
        self.episode_rewards += delta_reward
        self.update(state, action, next_state, delta_reward)

    def start_episode(self):
        """
        Called by environment when new episode is starting
        """
        self.episode_rewards = 0.0

    def stop_episode(self):
        """
        Called by environment when episode is done
        """
        if self.num_episodes_completed < self.num_training:
            self.accum_train_rewards += self.episode_rewards
        else:
            self.accum_test_rewards += self.episode_rewards
        self.num_episodes_completed += 1

        if self.num_episodes_completed >= self.num_training:
            self.exploration_rate = 0.0  # no exploration
            self.learning_rate = 0.0  # no learning

    def is_training(self):
        return self.num_episodes_completed < self.num_training

    def is_testing(self):
        return not self.is_training()
