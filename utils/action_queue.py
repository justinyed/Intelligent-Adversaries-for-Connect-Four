from collections import deque
from random import choice


class ActionQueue:
    """
    for Iterative Deepening
    """

    def __init__(self, iterable):
        self.__data = deque(iterable=sorted(iterable, reverse=True))

    def copy(self):
        return ActionQueue(self.__data.copy())

    def __len__(self):
        return len(self.__data)

    def get(self, i=None):
        if i is None:
            return self.__data.index(0)
        return self.__data.index(i)

    def pop(self):
        return self.__data.pop()

    def append(self, x: tuple) -> None:
        if len(x) != 2 and type(x[0]) in [int, float]:
            raise ValueError(f"x is not of length 2 or the first element is not a number")
        found = False
        value = int(x[0])

        for e in self.__data:
            if e[0] <= value:
                self.__data.insert(self.__data.index(e), (int(x[0]), x[1]))
                found = True
                break
        if not found:
            self.__data.insert(len(self), x)

    def extend(self, container: [list, tuple]):
        dirty = sorted(self.to_list() + list(container), reverse=True)
        found, clean = [], []
        for k, v in dirty:
            if v not in found:
                found.append(v)
                clean.append((k, v))
        self.__data = deque(iterable=clean)

    def to_list(self):
        return list([e for e in self.__data])

    def get_best(self):
        if len(self) == 0:
            return None
        best_value = int(self.__data[0][0])
        best_actions = []

        for i in range(len(self)):
            e = self.__data[i]
            if e[0] >= best_value:
                best_actions.append(e)
            else:
                break

        return choice(best_actions)[1]

    def __iter__(self):
        return iter(self.to_list())

    def __str__(self):
        return str(self.__data)

    @staticmethod
    def build_naive_action_queue(game, evaluation_function, current_player):
        value_action_pairs = list([(evaluation_function(game.get_successor_game(move), current_player), move)
                                   for move in game.get_legal_actions()])
        return ActionQueue(value_action_pairs)
