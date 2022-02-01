from game import Connect4
from time import sleep
from colorama import Fore


class Connect4CLI:
    """
    Command Line Interface for connect 4
    """

    def __init__(self):
        self.agent_1 = None
        self.agent_2 = None
        self.move = None  # Keep track of last move
        self.num_players = 2

    def start(self, starting_game=Connect4()):
        """
        Once initialize use this method to start the game
        """
        self.agent_1 = self.select_agent(starting_game, 1)
        self.agent_2 = self.select_agent(starting_game, -1)
        self.handler(starting_game)

    def handler(self, game):
        """
        The main method which handles orchestrating the game.
        """
        while True:
            print(self.get_display(game))
            if game.turn % self.num_players == 0:
                self.move = self.agent_1.get_action(game)
            else:
                self.move = self.agent_2.get_action(game)

            game.drop_piece(self.move)

            # check for terminal states
            if game.get_status() == game.tie:
                print(self.get_display(game))
                print("Tie Connect4!")
                break
            if game.is_terminal_state():
                print(self.get_display(game))
                player = game.get_current_player()
                print(
                    f"Player {Connect4CLI.player_number(game, player)} Won the Connect4!")
                break

    @staticmethod
    def player_number(game_state, piece):
        if game_state.player1 == piece:
            return 1
        else:
            return 2

    @staticmethod
    def select_agent(game_state, player):
        """
        Agent Selection Menu
        """
        menu = ""
        menu += "\n" * 50
        menu += "CONNECT 4\n"
        menu += "=" * 50 + "\n"
        menu += "AGENT SELECTION:\n"

        options = {"Human Player": Human()
                   }

        keys = list(options.keys())
        for i in range(len(keys)):
            menu += f"[{i}]\t{keys[i]}\n"

        print(menu)
        try:
            c = int(input(f"Select an option for Agent {Connect4CLI.player_number(game_state, player)}: "))
            return list(options.values())[c]

        except ValueError:
            print("Improper Input; Try Again")
            sleep(0.75)
            Connect4CLI.select_agent(game_state, player)
        except IndexError:
            print("Improper Input; Try Again")
            sleep(0.75)
            Connect4CLI.select_agent(game_state, player)
        except Exception as error:
            print(error)
            sleep(0.75)
            Connect4CLI.select_agent(game_state, player)

    @staticmethod
    def get_piece_representation(game, piece,
                                 empty=" ",
                                 player1=f"{Fore.BLUE}O{Fore.RESET}",
                                 player2=f"{Fore.RED}O{Fore.RESET}"):
        if piece == game.player1:
            return player1
        elif piece == game.player2:
            return player2
        else:
            return empty

    @staticmethod
    def get_grid_representation(game):
        """
        Build the Grid's Representation to be displayed
        """
        colors = [Fore.BLUE, Fore.RED, Fore.MAGENTA]
        current_player = game.get_current_player()

        if current_player == game.get_tie_code():
            representation = f"{colors[(current_player - 1)]}Tie Connect4!{Fore.RESET}\n"
        else:
            representation = f"{colors[(current_player - 1)]}Player {Connect4CLI.player_number(game, current_player)}'s{Fore.RESET} Turn\n"

        representation += f"turn={game.get_turn()} \n"
        representation += f"status={game.get_status()}\n"

        for y in range(game.get_board().height - 1, -1, -1):
            for x in range(game.get_board().width):
                piece = game.get_board().get_piece((x, y))
                representation += f"[{Connect4CLI.get_piece_representation(game, piece)}]"
            representation += "\n"
        return representation[:-1]

    def get_display(self, game_state):
        """
        Build the Full Round Display
        """
        menu = ""
        menu += "\n" * 50 + self.get_grid_representation(game_state) + "\n"

        # number line
        menu += "=" * (game_state.get_board().width * 3) + "\n"
        num_line = "["
        for i in range(1, game_state.get_board().width + 1):
            if self.move is not None and i == self.move + 1:
                num_line += f"{Fore.GREEN}{i}{Fore.RESET}]["
            else:
                num_line += f"{i}]["
        num_line = f"{num_line[:-2]}]"
        menu += f"{num_line}\n"
        return menu


class Human:
    """
    Handles a Human Player's Input
    """

    def get_action(self, game_state):
        try:
            move = int(input(
                f"Player {Connect4CLI.player_number(game_state, game_state.get_current_player())} ({Connect4CLI.get_piece_representation(game_state, game_state.get_current_player())}), drop in what column (1-7): ")) - 1
            if move not in game_state.get_legal_actions():
                raise ValueError()
            else:
                return move

        except ValueError:
            print("Column Out of Range; Try Again")
            sleep(0.75)
            self.get_action(game_state)


if __name__ == '__main__':
    g = Connect4CLI()
    g.start()
