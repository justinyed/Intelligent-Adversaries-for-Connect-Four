import numpy as np
from scipy.signal import convolve2d
from game import ConnectFour

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
kernels_4 = get_kernels(4)


def evaluation_function_conv(game: ConnectFour):
    """
    Uses Convolution method to evaluate the state of the game and returns the static value of being in that state.

    :param game: game state to evaluate
    :return: static value in current state
    """
    grid = game.get_board().get_grid()
    player = game.get_current_player()
    negative_grid = -1 * grid

    opponent_fours = check_line(negative_grid, player, kernels_4, 4).sum()
    if opponent_fours == 1:
        return NEGATIVE_INF

    fours = check_line(grid, player, kernels_4, 4).sum()
    if fours == 1:
        return POSITIVE_INF

    threes = check_line(grid, player, kernels_3, 3).sum() - (2 * fours)
    opponent_threes = check_line(negative_grid, player, kernels_3, 3).sum() - (2 * opponent_fours)

    twos = check_line(grid, player, kernels_2, 2).sum() - (2 * threes - 3 * fours)
    opponent_twos = check_line(negative_grid, player, kernels_2, 2).sum() - (2 * opponent_threes - 3 * opponent_fours)

    a = 300
    b = 30
    c = -600
    d = -20

    return a * threes + b * twos + c * opponent_threes + d * opponent_twos


def check_line(grid, current_player, kernels, n):
    g = grid == current_player
    return np.array(
        tuple(np.count_nonzero(convolve2d(g, kernel, mode="valid", fillvalue=0) == n) for kernel in kernels))
