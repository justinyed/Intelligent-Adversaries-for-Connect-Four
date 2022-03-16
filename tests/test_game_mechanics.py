import unittest
import ast
from os import listdir
from os.path import isfile, join
import numpy as np
from parameterized import parameterized

from src.game import ConnectFour
from src.board import TupleBoard
from src.interface_cli import ConnectFourCLI
from constants_cli import PLAYER1_COLOR, PLAYER2_COLOR, RESET_COLOR

PLAYER1 = 'X'
PLAYER2 = 'O'
EMPTY = ' '
REMINDER = f'P1={PLAYER1_COLOR}{PLAYER1}{RESET_COLOR}; P2={PLAYER2_COLOR}{PLAYER2}{RESET_COLOR}'
DIRECTORY = 'layouts'
BOARD_TYPE = TupleBoard


def state_from_string(layout, game_type=ConnectFour, board_type=BOARD_TYPE):
    """
    Designed to work with 1D tuple _board type, but could be modified for other types

    :param layout: string of the _board layout
    :param game_type: Class for the Game
    :param board_type: Class for the Board
    :return:
    """
    game = game_type(board_type=board_type)

    # Retrieve _grid
    grid_lines = layout.splitlines(keepends=False)[:6]
    raw_grid = list(reversed([row[1:].lstrip("[").rstrip("]").split("][") for row in grid_lines]))

    # create string _board
    str_grid = str(raw_grid) \
        .replace(f"'{PLAYER1}'", str(game.get_player1())) \
        .replace(f"'{PLAYER2}'", str(game.get_player2())) \
        .replace(f"'{EMPTY}'", str(game.get_default())) \
        .replace(f"]", "").replace(f"[", "")

    # create tuple _board
    grid = ast.literal_eval("(" + str_grid + ")")

    # create array _board from tuple _board
    grid_array = np.array(grid)
    grid_array = np.transpose(grid_array.reshape([6, 7]))

    # Build Board from set_piece function (agnostic to the backend of the _board)
    turn = 0
    board = board_type()
    for player in game.get_players():
        xs, ys = np.where(grid_array == player)
        xs, ys = tuple(xs), tuple(ys)
        positions = list(zip(xs, ys))
        for pos in positions:
            board.set_piece(position=pos, piece=player)
            turn += 1
    board.reindex_lowest()
    return board, turn, 0


def load_layout(filepath, game=ConnectFour(board_type=BOARD_TYPE)):
    try:
        with open(filepath, mode='r') as f:

            action = ast.literal_eval(f.readline().split("=")[1])
            expected_status = ast.literal_eval(f.readline().split("=")[1])

            board = f.read()
            state = state_from_string(board)
            game._set_state(state)

            return game, action, expected_status
    except Exception as e:
        print(e)
        return game


def get_test_layout(filepath):
    g, a, expected = load_layout(filepath)
    before = f"\nInitial State:\n{ConnectFourCLI.get_display_board(g)}"
    actual = g.perform_action(a)
    after = f"\nCurrent State:\n{ConnectFourCLI.get_display_board(g)}"
    msg = f"expected=\'{expected}\', but actual=\'{actual}\'\n" \
          f"{REMINDER}\n" \
          f"{before}\n" \
          f"\n### performed action '{a}' ###\n" \
          f"{after}\n{'='*35}"

    return actual, expected, msg


path = join('.', DIRECTORY)
files = [f for f in listdir(path) if isfile(join(path, f))]
params = list([[f'{file.split(".")[0]}', *get_test_layout(join('.', DIRECTORY, file))] for file in files])


class TestSequence(unittest.TestCase):
    @parameterized.expand(params)
    def test(self, name, a, b, c):
        self.assertEqual(a, b, c)
