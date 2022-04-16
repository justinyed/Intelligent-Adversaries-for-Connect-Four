from lru import LRU


class SuccessorGenerator:
    """Uses a LRU cache of max_size"""

    def __init__(self, max_size=100000):
        """
        Generate Successors of the game state and cache most used
        :param max_size: of the LRU Cache
        """
        self._cache = LRU(max_size)

    def get_successor(self, state, action):
        """
        Given an action and state return a new state.
        :param state: game state
        :param action: to be applied to state
        :return: new game state
        """
        h = hash((state, action))
        if h in self._cache:
            return self._cache[h]
        else:  # store
            g = state.get_successor(action)
            self._cache[h] = g
            return g


GENERATOR = SuccessorGenerator()
