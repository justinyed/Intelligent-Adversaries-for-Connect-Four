from lru import LRU
from functools import lru_cache
import cachetools


# todo fix cache
# class SuccessorGenerator:
#
#     def __init__(self, max_size=100000):
#         self._cache = LRU(max_size)

def get_successor(state, action):
    return state.get_successor(action)

    # h = state.get_board().hash_board(action)
    # if h in self._cache:
    #     return self._cache[h]
    # else:  # store
    #     g = state.get_successor(action)
    #     self._cache[h] = g
    #     return g

# GENERATOR = SuccessorGenerator()
