from lru import LRU


class SuccessorGenerator:

    def __init__(self, max_size=100000):
        self._cache = LRU(max_size)

    def get_successor(self, state, action):
        h = hash((state, action))
        if h in self._cache:
            return self._cache[h]
        else:  # store
            g = state.get_successor(action)
            self._cache[h] = g
            return g


GENERATOR = SuccessorGenerator()
