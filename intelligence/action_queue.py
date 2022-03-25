from collections import deque
from random import choice
from intelligence.successor_generator import get_successor


class ActionQueue:
    """
    for Iterative Deepening
    """

    def __init__(self, iterable):
        self.__data = deque(iterable=sorted(iterable, reverse=True))

    def copy(self):
        return ActionQueue(self.__data.copy())

    def get(self, i=None):
        if i is None:
            return self.__data[0]
        return self.__data[i]

    def pop(self):
        return self.__data.pop()

    def extend(self, container) -> None:
        if type(container) is ActionQueue:
            container = container.to_list()
        unclean = sorted(list(container) + self.to_list(), reverse=True)
        found, clean = [], []
        for value, action in unclean:
            if action not in found:
                found.append(action)
                clean.append((value, action))
        self.__data = deque(iterable=clean)

    def append(self, x: tuple) -> None:
        self.extend([x])

    def clear(self) -> None:
        self.__data.clear()

    def get_best_value_action_pair(self):
        if len(self) == 0:
            return None

        best_value, best_actions = self.get_best_value(), []

        for i in range(len(self)):
            e = self.__data[i]
            if e[0] == best_value:
                best_actions.append(e)
            else:
                break

        return choice(best_actions)

    def get_best_action(self):
        return self.get_best_value_action_pair()[1]

    def get_best_value(self):
        return self.__data[0][0]

    def to_list(self) -> list:
        return list([e for e in self.__data])

    def get_actions(self) -> list:
        return list([e[1] for e in self.__data])

    def get_values(self) -> list:
        return list([e[0] for e in self.__data])

    def __add__(self, other):
        self.extend(other)

    def __iter__(self):
        return iter(self.get_actions())

    def __str__(self):
        return str(self.__data)

    def __len__(self):
        return len(self.__data)

    def __reversed__(self):
        self.__data = reversed(self.__data)

    def __rand__(self, other):
        self.__add__(other)

    def __deepcopy__(self, memodict):
        return self.copy()

    def __hash__(self):
        return hash(self.__data)


def reflex_action_queue(game, evaluation_function, current_player):
    """
    The reflex action queue builds a list of value action pairs based on
    the static value of a game_components state as defined by an evaluation function.
    :param game: game_components state
    :param evaluation_function: evaluates the value of the game_components
    :param current_player: maximizing current_player
    :return: ActionQueue with value action pairs as defined above
    """

    value_action_pairs = list([(evaluation_function(get_successor(game, move), current_player), move)
                               for move in game.get_legal_actions()])

    return ActionQueue(value_action_pairs)
