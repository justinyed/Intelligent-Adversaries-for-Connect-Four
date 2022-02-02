from time import sleep
import constants_cli
from game import ConnectFour
from agent import Random, Reflex, Agent


def get_options(player):
    return {"Human Player": Human(player),
            "Random Agent": Random(player),
            "Reflex Agent": Reflex(player)
            }


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
        Once initialize use this method to start the game
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
            if game.turn % self.num_players == 0:
                self.move = self.agent_1.get_action(game)
                sleep(constants_cli.DROP_TIME)
            else:
                self.move = self.agent_2.get_action(game)
                print(self.move)
                sleep(constants_cli.DROP_TIME)

            game.drop_piece(self.move)

            # check for terminal states
            if game.get_status() == game.tie:
                print(self.get_display(game))
                print(constants_cli.TIE_MSG)
                break
            if game.is_terminal_state():
                print(self.get_display(game))
                player = game.get_current_player()
                print(f"Player {ConnectFourCLI.player_number(game, player)} {constants_cli.WIN_MSG}")
                break

    @staticmethod
    def player_number(game, piece):
        if game.player1 == piece:
            return constants_cli.PLAYER1
        else:
            return constants_cli.PLAYER2

    @staticmethod
    def select_agent(game, player):
        """
        Agent Selection Menu
        """
        menu = constants_cli.SELECT_AGENT_MSG

        options = get_options(player)

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
            ConnectFourCLI.select_agent(game, player)
        except Exception as error:
            print(error)
            sleep(constants_cli.BAD_INPUT_TIME)
            ConnectFourCLI.select_agent(game, player)

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
        """
        Build the Grid's Representation to be displayed
        """
        colors = [constants_cli.PLAYER1_COLOR, constants_cli.PLAYER2_COLOR, constants_cli.TIE_COLOR]
        current_player = game.get_current_player()

        if current_player == game.get_tie_code():
            representation = f"{colors[(current_player - 1)]}{constants_cli.TIE_MSG}{constants_cli.RESET_COLOR}\n"
        else:
            representation = f"{colors[(current_player - 1)]}Player {ConnectFourCLI.player_number(game, current_player)}'s{constants_cli.RESET_COLOR} Turn\n"

        representation += f"turn={game.get_turn()} \n" + f"status={game.get_status()}\n"

        for y in range(game.get_board().height - 1, -1, -1):
            for x in range(game.get_board().width):
                piece = game.get_board().get_piece((x, y))
                representation += f"[{ConnectFourCLI.get_display_piece(game, piece)}]"
            representation += "\n"
        return representation[:-1]

    def get_display(self, game):
        """
        Build the Full Round Display
        """
        menu = ""
        menu += "\n" * 50 + self.get_display_board(game) + "\n"

        # number line
        menu += "=" * (game.get_board().width * 3) + "\n"
        num_line = "["
        for i in range(1, game.get_board().width + 1):
            if self.move is not None and i == self.move + 1:
                num_line += f"{constants_cli.LAST_MOVE_COLOR}{i}{constants_cli.RESET_COLOR}]["
            else:
                num_line += f"{i}]["
        num_line = f"{num_line[:-2]}]"
        menu += f"{num_line}\n"
        return menu


class Human(Agent):
    """Handles a Human Player's Input"""

    def get_action(self, game):
        try:
            move = int(input(
                f"Player {ConnectFourCLI.player_number(game, game.get_current_player())} ("
                f"{ConnectFourCLI.get_display_piece(game, game.get_current_player())}"
                f"), drop in what column (1-7): "))
            move -= 1

            if move not in game.get_legal_actions():
                raise ValueError()
            else:
                return move

        except ValueError:
            print(constants_cli.ILLEGAL_INPUT_MSG)
            sleep(constants_cli.BAD_INPUT_TIME)
            self.get_action(game)


if __name__ == '__main__':
    ConnectFour = ConnectFourCLI()
    ConnectFour.start()
