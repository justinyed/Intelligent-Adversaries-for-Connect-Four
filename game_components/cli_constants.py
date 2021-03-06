from colorama import Fore
import game_components.cli_human_input
import intelligence.agent as agent
import intelligence.search_agents as search_agent


def agent_options():
    return {
        "Human Player": game_components.cli_human_input.Human(),
        "Random Agent": agent.Random(),
        "Reflex Agent": agent.Reflex(),
        "Minimax Agent": search_agent.MiniMax(depth_limit=3),
        "Alpha-Beta Agent": search_agent.AlphaBeta(depth_limit=3),
        "Iterative Agent": search_agent.IterativeDeepening(depth_limit=6)
    }


# Messages
WIN_MSG = "Won the Connect Four Game!"
TIE_MSG = "Tied the Connect Four Game."
BAD_INPUT_MSG = "Improper Input; Try Again"
ILLEGAL_INPUT_MSG = "Column Out of Range; Try Again"
BAD_INPUT_TIME = 0.75
CLEAR_MSG = "\n" * 50
LINE_MSG = "=" * 32
SELECT_AGENT_MSG = CLEAR_MSG + "CONNECT 4\n" + LINE_MSG + "\n" + "AGENT SELECTION:\n"

# Colors
PLAYER1_COLOR = Fore.BLUE
PLAYER2_COLOR = Fore.RED
LAST_MOVE_COLOR = Fore.GREEN
TIE_COLOR = Fore.MAGENTA
RESET_COLOR = Fore.RESET
COLORS = [PLAYER1_COLOR, PLAYER2_COLOR, TIE_COLOR]

# Pieces
PIECE = "O"
EMPTY_PIECE = " "
PLAYER1_PIECE = f"{PLAYER1_COLOR}{PIECE}{RESET_COLOR}"
PLAYER2_PIECE = f"{PLAYER2_COLOR}{PIECE}{RESET_COLOR}"

# Other
NUM_PLAYERS = 2
PLAYER1 = 1
PLAYER2 = 2
DROP_TIME = 0.75
