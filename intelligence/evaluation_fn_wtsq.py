import numpy as np
from game_components.game import PLAYER2
from game_components.connect_four import ConnectFour

"""
The value of each line is the sum of the values of its 4 individual squares, 
and the value of the _board is the sum of the values of the 69 potential winning lines. 
In other words, each square is weighted according to the number of unique winning lines it can be a member of
Found This Idea here: https://web.stonehill.edu/compsci/CS211/Assignments%202018/assignment%206.htm
The articles says that it originally came from a paper by Martin Stenmark.
"""
WEIGHTS = np.array([[3, 4, 5, 7, 5, 4, 3],
                    [4, 6, 8, 10, 8, 6, 4],
                    [5, 8, 11, 13, 11, 8, 5],
                    [5, 8, 11, 13, 11, 8, 5],
                    [4, 6, 8, 10, 8, 6, 4],
                    [3, 4, 5, 7, 5, 4, 3]])


WINNING_VALUE = (10.0 ** 9) * np.sum(WEIGHTS)
LOSING_VALUE = -1 * (10.0 ** 6) * np.sum(WEIGHTS)
TIE_VALUE = -1 * (10.0 ** 3) * np.sum(WEIGHTS)


def evaluation_function_weighted_square(game: ConnectFour, current_player: int):
    """
    Uses the 69 unique line method by Martin Stenmark to evaluate the state of the game_components and
    returns the static value of being in that state.
    Acts as a heuristic and evaluation function.

    :param current_player:
    :param game: game_components state to evaluate
    :return: static value in current state
    """

    # Check for terminal state
    if game.get_status() == current_player:
        return (1 / (game.get_turn() + 1)) * WINNING_VALUE  # without the living penalty it trolls the opponent
    elif game.is_tie():
        return TIE_VALUE
    elif game.is_terminal_state():
        return (1 / (game.get_turn() + 1)) * LOSING_VALUE  # todo - not sure about this part

    grid = game.get_board().get_grid()

    if current_player == PLAYER2:  # neutralize grid
        grid *= -1

    return np.sum(WEIGHTS * grid)
