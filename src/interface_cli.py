from time import sleep
from utils import constants_cli
from game import ConnectFour
from agent import Agent
from sys import getsizeof


class ConnectFourCLI:
    """
    Command Line Interface for Connect Four
    """

    def __init__(self):
        self.agent_1 = None
        self.agent_2 = None
        self.move = None  # Keep track of last move
        self.num_players = constants_cli.NUM_PLAYERS

    def start(self, game=ConnectFour()):
        """
        Once initialized, use this method to start the game
        """
        self.agent_1 = self.select_agent(game, constants_cli.PLAYER1)
        self.agent_2 = self.select_agent(game, constants_cli.PLAYER2)
        self.handler(game)

    def handler(self, game):
        """
        The main method which handles orchestrating the game.
        """
        while True:
            print(self.get_display(game))
            try:
                if game.turn % self.num_players == 0:
                    self.move = self.agent_1.get_action(game)
                    sleep(constants_cli.DROP_TIME)
                else:
                    self.move = self.agent_2.get_action(game)
                    sleep(constants_cli.DROP_TIME)

            except (ValueError, TypeError):
                print(constants_cli.ILLEGAL_INPUT_MSG)
                sleep(constants_cli.BAD_INPUT_TIME)
                self.handler(game)

            game.drop_piece(self.move)
            print(game.get_board().__hash__())
            print(getsizeof(game.get_board().__hash__()))

            # check for terminal states
            if game.get_status() == game.tie:
                print(self.get_display(game))
                print(constants_cli.TIE_MSG)
                break
            if game.is_terminal_state():
                print(self.get_display(game))
                player = game.get_current_player()
                msg = f"{constants_cli.COLORS[(player - 1)]}Player " + \
                      f"{ConnectFourCLI.player_number(game, player)} " + \
                      f"{constants_cli.WIN_MSG}{constants_cli.RESET_COLOR}"
                print(msg)
                break

    @staticmethod
    def player_number(game, piece):
        if game.player1 == piece:
            return constants_cli.PLAYER1
        else:
            return constants_cli.PLAYER2

    def select_agent(self, game, player) -> Agent:
        """
        Agent Selection Menu
        """
        menu = constants_cli.SELECT_AGENT_MSG

        options = constants_cli.agent_options(player)

        keys = list(options.keys())
        for i in range(len(keys)):
            menu += f"[{i}]\t{keys[i]}\n"

        print(menu)
        try:
            c = int(input(f"Select an option for Agent {ConnectFourCLI.player_number(game, player)}: "))
            return list(options.values())[c]

        except (IndexError, ValueError):
            print(constants_cli.BAD_INPUT_MSG)
            sleep(constants_cli.BAD_INPUT_TIME)
            return self.select_agent(game, player)


    def get_display(self, game):
        """Build the Full Display for the round"""
        return constants_cli.CLEAR_MSG + ConnectFourCLI.get_display_board(game) + "\n" + \
               self.__get_display_numbers(game) + "\n"

    @staticmethod
    def get_display_piece(game, piece):
        if piece == game.player1:
            return constants_cli.PLAYER1_PIECE
        elif piece == game.player2:
            return constants_cli.PLAYER2_PIECE
        else:
            return constants_cli.EMPTY_PIECE

    @staticmethod
    def get_display_board(game):
        """Build the Grid's Representation to be displayed"""
        current_player = game.get_current_player()

        representation = ""

        if current_player in game.get_players():
            representation += f"{constants_cli.COLORS[(current_player - 1)]}Player " + \
                              f"{ConnectFourCLI.player_number(game, current_player)}'s" + \
                              f"{constants_cli.RESET_COLOR} Turn\n"

        representation += f"turn={game.get_turn()} \n" + f"status={game.get_status()}\n"

        for y in range(game.get_board().height - 1, -1, -1):
            for x in range(game.get_board().width):
                piece = game.get_board().get_piece((x, y))
                representation += f"[{ConnectFourCLI.get_display_piece(game, piece)}]"
            representation += "\n"
        return representation[:-1]

    def __get_display_numbers(self, game):
        """Build number line with last played move highlighted"""
        num_line = "=" * (game.get_board().width * 3) + "\n"
        num_line += "["
        for i in range(1, game.get_board().width + 1):
            if self.move is not None and i == self.move + 1:
                num_line += f"{constants_cli.LAST_MOVE_COLOR}{i}{constants_cli.RESET_COLOR}]["
            else:
                num_line += f"{i}]["
        num_line = f"{num_line[:-2]}]"
        return num_line


class Human(Agent):
    """Handles a Human Player's Input"""

    def get_action(self, game):
        player = game.get_current_player()
        move = int(input(
            f"Player {ConnectFourCLI.player_number(game, player)} ("
            f"{ConnectFourCLI.get_display_piece(game, player)}"
            f"), drop in what column (1-7): "))
        move -= 1

        if move in game.get_legal_actions():
            return move
        else:
            raise ValueError()


if __name__ == '__main__':
    ConnectFour = ConnectFourCLI()
    ConnectFour.start()
