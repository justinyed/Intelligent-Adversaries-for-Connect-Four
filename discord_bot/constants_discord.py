from src.game import ConnectFour, PLAYER1, PLAYER2, EMPTY
from discord import Button, ButtonStyle, ActionRow, SelectOption, SelectMenu
import intelligence

NUM_PLAYERS = 2
DROP_TIME = 0.0
ILLEGAL_INPUT_MSG = ""
BAD_INPUT_TIME = 0.7

ADMINS = ["justinyedinak#2425"]

CLG_DESCRIPTION = 'Challenge a current_player or agent by providing the ID. ' \
                  'If no parameter is given, then a menu will assist.'

BUTTONS = [
    ActionRow(*list([Button(label=f"{i}", custom_id=f"{i}", style=ButtonStyle.blurple) for i in range(1, 5)])),
    ActionRow(*(list([Button(label=f"{i}", custom_id=f"{i}", style=ButtonStyle.blurple) for i in range(5, 8)])
                + [Button(label="\t", custom_id="empty", style=ButtonStyle.blurple, disabled=True)]))
]

ACCEPT_REJECT_BUTTONS = [Button(label='Accept', custom_id='accept', style=ButtonStyle.green),
                         Button(label='Reject', custom_id='reject', style=ButtonStyle.red)]

AGENTS = {
    "Random_Agent": intelligence.Random(),
    "Reflex_Agent": intelligence.Reflex(),
    "Minimax_Agent": intelligence.MiniMax(depth_limit=2),
    "AlphaBeta_Agent": intelligence.AlphaBeta(depth_limit=3),
    "Iterative_Agent": intelligence.IterativeDeepening(depth_limit=4)
}

AGENT_MENU = [
    SelectMenu(custom_id='_select_it',
               options=list([SelectOption(label=agent, value=agent) for agent in AGENTS.keys()]),
               placeholder='Select some Options', max_values=1)
]

# ### Visual Components ###
PLAYER1_PIECE = ":regional_indicator_x:"
PLAYER2_PIECE = ":o2:"
EMPTY_PIECE = ":white_large_square:"
structure = ":yellow_square:"

PIECES = {
    EMPTY: EMPTY_PIECE,
    PLAYER1: PLAYER1_PIECE,
    PLAYER2: PLAYER2_PIECE
}

ONE = ":one:"
TWO = ":two:"
THREE = ":three:"
FOUR = ":four:"
FIVE = ":five:"
SIX = ":six:"
SEVEN = ":seven:"

BUTTON_NUMBERS = (ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN)
BUTTON_DECODER = dict(zip(BUTTON_NUMBERS, range(len(BUTTON_NUMBERS))))
