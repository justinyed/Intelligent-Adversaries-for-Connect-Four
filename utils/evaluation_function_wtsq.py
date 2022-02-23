import numpy as np
from game import ConnectFour, PLAYER1, PLAYER2, EMPTY, TIE_CODE

POSITIVE_INF = float("inf")
NEGATIVE_INF = float("-inf")
WINNING_VALUE = POSITIVE_INF
LOSING_VALUE = NEGATIVE_INF

"""
The value of each line is the sum of the values of its 4 individual squares, 
and the value of the board is the sum of the values of the 69 potential winning lines. 
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


def evaluation_function_weighted_square(game: ConnectFour, current_player: int):
    """
    Uses the 69 unique line method by Martin Stenmark to evaluate the state of the game and
    returns the static value of being in that state.
    Acts as a heuristic and evaluation function.

    :param current_player:
    :param game: game state to evaluate
    :return: static value in current state
    """
    # Check for terminal state
    if game.get_status() is current_player:
        return WINNING_VALUE
    elif game.is_terminal_state():
        return LOSING_VALUE

    grid = game.get_board().get_grid()

    if current_player is PLAYER2:  # neutralize grid
        grid *= -1

    return np.sum(WEIGHTS * grid)
