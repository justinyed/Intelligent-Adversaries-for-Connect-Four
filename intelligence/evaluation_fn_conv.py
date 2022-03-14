import numpy as np
from scipy.signal import convolve2d
from game import ConnectFour, PLAYER1, PLAYER2, EMPTY, TIE_CODE

POSITIVE_INF = float("inf")
NEGATIVE_INF = float("-inf")


def get_kernels(n=4):
    horizontal_kernel = np.array([[1 for _ in range(n)]], dtype=int)
    vertical_kernel = np.transpose(horizontal_kernel)
    diag1_kernel = np.eye(n, dtype=int)
    diag2_kernel = np.fliplr(diag1_kernel)
    return [horizontal_kernel, vertical_kernel, diag1_kernel, diag2_kernel]


kernels_2 = get_kernels(2)
kernels_3 = get_kernels(3)


def evaluation_function_conv(game: ConnectFour, current_player: int):
    """
    Uses Convolution method to evaluate the state of the game and returns the static value of being in that state.
    Acts as a heuristic and evaluation function.

    :param current_player:
    :param game: game state to evaluate
    :return: static value in current state
    """
    grid = game.get_board().get_grid()
    negative_grid = -1 * grid

    # Check for terminal state
    if game.get_status() is current_player:
        return POSITIVE_INF
    elif game.is_terminal_state():
        return NEGATIVE_INF

    threes = check_line(grid, current_player, kernels_3, 3).sum()
    opponent_threes = check_line(negative_grid, current_player, kernels_3, 3).sum()

    twos = check_line(grid, current_player, kernels_2, 2).sum() - (2 * threes)
    opponent_twos = check_line(negative_grid, current_player, kernels_2, 2).sum() - (2 * opponent_threes)

    a = 300
    b = -600
    c = 30
    d = -20

    return a * threes + b * opponent_threes + c * twos + d * opponent_twos


def check_line(grid, current_player, kernels, n):
    g = grid == current_player
    return np.array(
        tuple(np.count_nonzero(convolve2d(g, kernel, mode="valid", fillvalue=0) == n) for kernel in kernels))
