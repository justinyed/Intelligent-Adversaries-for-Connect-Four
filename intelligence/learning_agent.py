from abc import ABC
import intelligence.agent


class Learning(intelligence.agent.Agent, ABC):

    def __init__(self, learning_rate: float = 1.0, exploration_rate: float = 0.05, discount_factor: float = 0.8,
                 iterations: int = 10):
        """

        :param learning_rate:
        :param exploration_rate:
        :param discount_factor:
        :param iterations:
        """
        super().__init__()
        self.learning_rate = learning_rate
        self.exploration_rate = exploration_rate
        self.discount_factor = discount_factor
        self.iterations = iterations
        self.current_iteration = 0



