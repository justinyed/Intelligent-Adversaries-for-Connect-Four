from time import sleep
import game_components.cli_constants as constant
import game_components.connect_four as c4


class ConnectFourCLI:
    """
    Command Line Interface for Connect Four
    """

    def __init__(self):
        self.agent_1 = None
        self.agent_2 = None
        self.move = None  # Keep track of last move
        self.num_players = constant.NUM_PLAYERS

    def start(self, game=c4.ConnectFour()):
        """
        Once initialized, use this method to start the game
        """
        self.agent_1 = self.select_agent(game, 1)
        self.agent_2 = self.select_agent(game, -1)  # player must be same as encoding
        self.handler(game)

    def handler(self, game):
        """
        The main method which handles orchestrating the game
        """

        while True:
            print(self.get_display(game))
            try:
                if game.get_turn() % self.num_players == 0:
                    self.move = self.agent_1.get_action(game)
                    sleep(constant.DROP_TIME)
                else:
                    self.move = self.agent_2.get_action(game)
                    sleep(constant.DROP_TIME)

            except (ValueError, TypeError):
                print(constant.ILLEGAL_INPUT_MSG)
                sleep(constant.BAD_INPUT_TIME)
                self.handler(game)

            print("Performing Action:", self.move)
            game.perform_action(self.move)

            # check for terminal states
            if game.is_tie():
                print(self.get_display(game))
                print(constant.TIE_MSG)
                return
            if game.is_terminal_state():
                print(self.get_display(game))
                player = game.get_current_player()
                msg = f"{constant.COLORS[(player - 1)]}Player " + \
                      f"{ConnectFourCLI.player_number(game, player)} " + \
                      f"{constant.WIN_MSG}{constant.RESET_COLOR}"
                print(msg)
                return

    @staticmethod
    def player_number(game, piece):
        if game.get_player1() == piece:
            return constant.PLAYER1
        else:
            return constant.PLAYER2

    def select_agent(self, game, player):
        """
        Agent Selection Menu
        """
        menu = constant.SELECT_AGENT_MSG

        options = constant.agent_options()

        keys = list(options.keys())
        for i in range(len(keys)):
            menu += f"[{i}]\t{keys[i]}\n"

        print(menu)
        try:
            choice = int(input(f"Select an option for Agent {ConnectFourCLI.player_number(game, player)}: "))
            return list(options.values())[choice]

        except (IndexError, ValueError):
            print(constant.BAD_INPUT_MSG)
            sleep(constant.BAD_INPUT_TIME)
            return self.select_agent(game, player)

    def get_display(self, game):
        """Build the Full Display for the round"""
        return constant.CLEAR_MSG + ConnectFourCLI.get_display_board(game) + "\n" + \
               self.__get_display_numbers(game) + "\n"

    @staticmethod
    def get_display_piece(game, piece):
        if piece == game.get_player1():
            return constant.PLAYER1_PIECE
        elif piece == game.get_player2():
            return constant.PLAYER2_PIECE
        else:
            return constant.EMPTY_PIECE

    @staticmethod
    def get_display_board(game):
        """Build the Grid's Representation to be displayed"""
        current_player = game.get_current_player()

        representation = ""

        if current_player in game.get_players():
            representation += f"{constant.COLORS[(current_player - 1)]}Player " + \
                              f"{ConnectFourCLI.player_number(game, current_player)}'s" + \
                              f"{constant.RESET_COLOR} Turn\n"

        representation += f"turn={game.get_turn()} \n" + f"status={game.get_status()}\n"

        for y in range(game.get_board().get_height() - 1, -1, -1):
            for x in range(game.get_board().get_width()):
                piece = game.get_board().get_piece((x, y))
                representation += f"[{ConnectFourCLI.get_display_piece(game, piece)}]"
            representation += "\n"
        return representation[:-1]

    def __get_display_numbers(self, game):
        """Build number line with last played move highlighted"""
        num_line = "=" * (game.get_board().get_width() * 3) + "\n"
        num_line += "["
        for i in range(1, game.get_board().get_width() + 1):
            if self.move is not None and i == self.move + 1:
                num_line += f"{constant.LAST_MOVE_COLOR}{i}{constant.RESET_COLOR}]["
            else:
                num_line += f"{i}]["
        num_line = f"{num_line[:-2]}]"
        return num_line


if __name__ == '__main__':
    ConnectFour = ConnectFourCLI()
    ConnectFour.start()
