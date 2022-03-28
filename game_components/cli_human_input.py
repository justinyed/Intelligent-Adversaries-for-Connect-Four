import game_components.cli_interface as interface
from intelligence import agent as agent


class Human(agent.Agent):
    """Handles a Human Player's Input"""

    def _get_action(self, game, time_start):
        player = game.get_current_player()
        move = int(input(
            f"Player {interface.ConnectFourCLI.player_number(game, player)} ("
            f"{interface.ConnectFourCLI.get_display_piece(game, player)}"
            f"), drop in what column (1-7): "))
        move -= 1

        if move in game.get_legal_actions():
            return move
        else:
            raise ValueError()
