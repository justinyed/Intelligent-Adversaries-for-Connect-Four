import unittest
import numpy as np
from src.game import ConnectFour
from src.board import TupleBoard
import ast
from os import listdir
from os.path import isfile, join, sep, basename

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
    layout = str(layout)

    game = game_type(board_type=TupleBoard)

    # Retrieve grid
    grid_lines = layout.splitlines(keepends=False)

    raw_grid = list(reversed([row[1:].lstrip("[").rstrip("]").split("][") for row in grid_lines]))

    str_grid = str(raw_grid) \
        .replace(f"'{PLAYER1}'", str(game.player1)) \
        .replace(f"'{PLAYER2}'", str(game.player2)) \
        .replace(f"'{EMPTY}'", str(game.get_board().default)) \
        .replace(f"]", "").replace(f"[", "")

    cnt_player1 = str_grid.count(PLAYER1)
    cnt_player2 = str_grid.count(PLAYER2)
    turn = cnt_player1 + cnt_player2 + 1

    grid = ast.literal_eval("(" + str_grid + ")")
    return board_type(grid=grid), turn, 0


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
    grid = game.get_board().get_grid()
    if type(grid) in (tuple, list):
        grid = np.array(list(reversed(grid)))
    if len(np.shape(grid)) == 1:
        grid = np.fliplr(grid.reshape([6, 7]))
    return str(grid)


def get_test_layout(file):
    g, a, expected = load_layout(file)
    actual = g.drop_piece(a)
    msg = f"expected=\'{expected}\', but actual=\'{actual}\'\n" + get_board_str(g)
    return actual, expected, msg


def fn(i): ...


output = ...


class TestSequence(unittest.TestCase):
    pass


for i in range(1, 11):
    test_method_name = 'test_fn_{0}'.format(i)
    testmethod = lambda self: self.assertEqual(fn(i), output[i])
    setattr(TestSequence, test_method_name, testmethod)

path = join('.', DIRECTORY)
        files = [f for f in listdir(path) if isfile(join(path, f))]
        for file in files:
            file_name = basename(file)
            print(f'Test Layout {file_name}')
            self.assertEqual(*get_test_layout(join('.', DIRECTORY, file)))



class TestGameMechanics(unittest.TestCase):
    pass
    def test_mechanics(self):



if __name__ == '__main__':
    unittest.main()
