import unittest
import numpy as np
from src.game import ConnectFour
from src.board import TupleBoard
from src.interface_cli import ConnectFourCLI
import ast
from os import listdir
from os.path import isfile, join

PLAYER1 = 'X'
PLAYER2 = 'O'
EMPTY = ' '
DIRECTORY = "layouts"


def state_from_string(layout, game_type=ConnectFour, board_type=TupleBoard):
    """
    Designed to work with 1D tuple board type, but could be modified for other types

    :param layout: string of the board layout
    :param game_type: Class for the Game
    :param board_type: Class for the Board
    :return:
    """
    game = game_type(board_type=TupleBoard)

    # Retrieve grid
    grid_lines = layout.splitlines(keepends=False)[:6]
    raw_grid = list(reversed([row[1:].lstrip("[").rstrip("]").split("][") for row in grid_lines]))

    # create string board
    str_grid = str(raw_grid) \
        .replace(f"'{PLAYER1}'", str(game.player1)) \
        .replace(f"'{PLAYER2}'", str(game.player2)) \
        .replace(f"'{EMPTY}'", str(game.get_board().default)) \
        .replace(f"]", "").replace(f"[", "")

    # create tuple board
    grid = ast.literal_eval("(" + str_grid + ")")

    # create array board from tuple board
    grid_array = np.array(grid)
    grid_array = np.transpose(grid_array.reshape([6, 7]))

    # Build Board from set_piece function (agnostic to the backend of the board)
    turn = 0
    board = board_type()
    for player in game.get_players():
        xs, ys = np.where(grid_array == player)
        xs, ys = tuple(xs), tuple(ys)
        positions = list(zip(xs, ys))
        for pos in positions:
            board.set_piece(position=pos, piece=player)
            turn += 1

    return board, turn, 0


def load_layout(file, game=ConnectFour(board_type=TupleBoard)):
    try:
        with open(file, mode='r') as f:

            action = ast.literal_eval(f.readline().split("=")[1])
            expected_status = ast.literal_eval(f.readline().split("=")[1])

            board = f.read()
            state = state_from_string(board)
            game.set_state(state)

            return game, action, expected_status
    except Exception as e:
        print(e)
        return game


def get_board_str(game):
    """
    Theoretically should handle 1D or 2D tuple or list
    May also work with a numpy array.

    :param game:
    :return:
    """
    return ConnectFourCLI.get_display_board(game)


def get_test_layout(file):
    g, a, expected = load_layout(file)
    actual = g.drop_piece(a)
    msg = f"expected=\'{expected}\', but actual=\'{actual}\'\n" + get_board_str(g)
    return actual, expected, msg


class TestGameMechanics(unittest.TestCase):
    pass


# found out how to use unittest using a loop
path = join('.', DIRECTORY)
files = [f for f in listdir(path) if isfile(join(path, f))]
for file in files:
    test_method_name = f'test_fn_{file.split(".")[0]}'
    test_info = get_test_layout(join('.', DIRECTORY, file))
    test_method = lambda self: self.assertEqual(*test_info)
    # define the TestGameMechanics Function
    setattr(TestGameMechanics, test_method_name, test_method)

if __name__ == '__main__':
    unittest.main()
