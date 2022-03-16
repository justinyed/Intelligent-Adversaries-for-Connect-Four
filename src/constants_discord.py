from game import ConnectFour, PLAYER1, PLAYER2, EMPTY

NUM_PLAYERS = 2
DROP_TIME = 0.0
ILLEGAL_INPUT_MSG = ""
BAD_INPUT_TIME = 0.7

CLG_DESCRIPTION = 'Challenge a current_player or agent by providing the ID. ' \
                  'If no parameter is given, then a menu will assist.'


# ### Visual Components ###
PLAYER1_PIECE = ":regional_indicator_x:"
PLAYER2_PIECE = ":o2:"
EMPTY_PIECE = ":white_large_square:"

PIECES = {
    EMPTY: EMPTY_PIECE,
    PLAYER1: PLAYER1_PIECE,
    PLAYER2: PLAYER2_PIECE
}

ONE = u"\u2474"
TWO = u"\u2475"
THREE = u"\u2476"
FOUR = u"\u2477"
FIVE = u"\u2478"
SIX = u"\u2479"
SEVEN = u"\u247A"

BUTTON_NUMBERS = (ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN)
BUTTON_DECODER = dict(zip(BUTTON_NUMBERS, range(len(BUTTON_NUMBERS))))