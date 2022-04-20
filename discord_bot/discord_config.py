from discord import Button, ButtonStyle, ActionRow, SelectOption, SelectMenu
import intelligence

ADMINS = ["justinyedinak#2425"]
DATABASE = "./leaderboard.db"

CLG_DESCRIPTION = 'Challenge a Current Player or Bot by providing the ID. ' \
                  'If no parameter is given, then a menu will assist.'

FORFEIT = 'forfeit'
FORFEIT_BUTTON = [Button(label="Quit", custom_id=FORFEIT, style=ButtonStyle.blurple)]


DISABLED_BUTTON = [Button(label="\t", custom_id="empty", style=ButtonStyle.blurple, disabled=True)]

PLAY_BUTTONS = [
    ActionRow(*list([Button(label=f"{i}", custom_id=f"{i}", style=ButtonStyle.blurple) for i in range(1, 5)])),
    ActionRow(*(list([Button(label=f"{i}", custom_id=f"{i}", style=ButtonStyle.blurple) for i in range(5, 8)])
                + FORFEIT_BUTTON))
]

ACCEPT_REJECT_BUTTONS = [Button(label='Accept', custom_id='accept', style=ButtonStyle.green),
                         Button(label='Reject', custom_id='reject', style=ButtonStyle.red)]

AGENTS = {
    "Easy"  : intelligence.IterativeDeepening(depth_limit=1, time_limit=3.0),
    "Medium": intelligence.IterativeDeepening(depth_limit=2, time_limit=3.0),
    "Hard"  : intelligence.IterativeDeepening(depth_limit=3, time_limit=4.0),
    "Elite" : intelligence.IterativeDeepening(depth_limit=5, time_limit=4.0),
}

AGENT_MENU = [
    SelectMenu(custom_id='_select_it',
               options=list([SelectOption(label=agent, value=agent) for agent in AGENTS.keys()]),
               placeholder='Select an Agent', max_values=1)
]


class TIME:
    rejection_timeout = 5
    challenge_timeout_message = 5
    challenge_timeout = 15


# ### Visual Components ###
PLAYER1_PIECE = ":regional_indicator_x:"
PLAYER2_PIECE = ":o2:"
EMPTY_PIECE = ":white_large_square:"
structure = ":yellow_square:"

PIECES = {
    0: EMPTY_PIECE,
    1: PLAYER1_PIECE,
    -1: PLAYER2_PIECE
}

DISPLAY_NUMBERS = (":one:", ":two:", ":three:", ":four:", ":five:", ":six:", ":seven:")


class MESSAGE:
    tie = 'The game has been Tied.'
    select_agent = 'Select an Artificially Intelligent Adversary'
    welcome = "Welcome to Connect Four!"
    turn_prompt = "Make a Selection"

    @staticmethod
    def tell_turn_start(challenger, piece):
        return f"It is {challenger}'s ( {piece} ) turn."

    @staticmethod
    def tell_challenge(challenger, opponent):
        return f"{opponent}, {challenger} has challenged you to a Connect Four Match."

    @staticmethod
    def tell_winner(player):
        return f"{player} has Triumphed!"

    @staticmethod
    def tell_challenger_declined(opponent):
        return f"{opponent} has rejected the challenge."

    @staticmethod
    def tell_challenger_timed_out(opponent):
        return f"{opponent} has not responded to the challenge."

    @staticmethod
    def tell_challenger_self(challenger):
        return f"@{challenger}, you cannot challenge yourself."
