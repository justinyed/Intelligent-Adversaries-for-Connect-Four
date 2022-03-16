
import os
from time import sleep
import uuid
import discord
from discord.ext import commands
import constants_discord as constant
from game import ConnectFour, PLAYER1, PLAYER2, EMPTY

TOKEN = os.getenv("DISCORD_TOKEN")

print('getcwd:      ', os.getcwd())
print('__file__:    ', __file__)

# import intelligence

class ConnectFourBot(commands.Bot):

    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix, **options)
        self.games = {}
        self.last_moves = {}
        self.agent1 = {}
        self.agent2 = {}
        self.channels = {}
        print(f"discord.py version={discord.__version__}")
        print(f"{self.user} is connected\n")

    @commands.command(name='challenge', aliases=['clg'],
                  description=constant.CLG_DESCRIPTION, help='help', pass_contaxt=True)
    async def challenge(self, ctx, opponent=None):
        """
        Allows the player to challenge an opponent
        :param ctx: context
        :param opponent: opponent player to challenge; if none options are given.
        """
        if opponent is None:  # Normally print dialog and request more info
            opponent = "Alpha-Beta Agent"
            await self.cfb_new(ctx.message.author, opponent, ctx.message.channel)
        else:
            await ctx.send(f"Challenge {opponent}")

    async def cfb_new(self, challenger, opponent, channel):
        game_id = uuid.uuid1()
        self.games[game_id] = ConnectFour()
        self.agent1[game_id] = challenger
        self.agent2[game_id] = opponent
        self.last_moves[game_id] = None
        self.channels[game_id] = channel

    async def game_handler(self, challenger, opponent, message, move):
        """
        Handles turns of game
        :param challenger:
        :param opponent:
        :param message:
        :param move:
        :return:
        """
        # SETUP
        print("ttt_move:{0}".format(challenger.id))
        uid = challenger.id
        if uid not in self.games:
            print("New game")
            await self.cfb_new(challenger, opponent, message.channel)

        game = self.games[challenger]

        # DISPLAY BOARD
        self.assemble_board(challenger)

        # REQUEST MOVE
        try:
            if game.get_turn() % constant.NUM_PLAYERS == 0:
                self.last_moves[challenger] = self.agent1[challenger].get_action(game)
                sleep(constant.DROP_TIME)
            else:
                self.last_moves[challenger] = self.agent2[challenger].get_action(game)
                sleep(constant.DROP_TIME)

        except (ValueError, TypeError):
            print(constant.ILLEGAL_INPUT_MSG)
            sleep(constant.BAD_INPUT_TIME)
            await self.game_handler(challenger, opponent, message, move)

        # MAKE MOVE
        game.drop_piece(self.last_moves[challenger])

        # CHECK TERMINAL STATE
        if game.get_status() == game._tie:  # TIE
            pass
        if game.is_terminal_state():  # WIN
            player = game.get_current_player()
            print(f"Player {player} Won!")

        # UPDATE BOARD
        await self.bot.edit_message(message, new_content=self.assemble_board(challenger))
        await self.game_handler(challenger, opponent, message, move)

    def assemble_board(self, game):
        """
        Create the representation of the game
        :param game: game state
        :return: string representation of the game
        """
        representation = ""
        for y in range(game.get_board().get_height() - 1, -1, -1):
            for x in range(game.get_board().get_width()):
                piece = game.get_board().get_piece((x, y))
                representation += f"{constant.PIECES[piece]}"
            representation += "\n"
        return representation


# class Human(intelligence.Agent):
#     """Handles a Human Player's Input"""
#
#     def __init__(self, player_number, player_id):
#         super().__init__(player_number)
#
#     def get_action(self, game):
#         player = game.get_current_player()
#
#         move = None
#
#         if move in game.get_legal_actions():
#             return move
#         else:
#             raise ValueError()

    # async def assemble_buttons(self, bot, msg):
    #     """
    #     Create reaction buttons
    #     :param bot:
    #     :param msg:
    #     :return:
    #     """
    #     for n in constant.BUTTON_NUMBERS:
    #         await bot.add_reaction(msg, n)
    #
    # async def on_reaction_add(self, bot, reaction, challenger):
    #     """
    #
    #     :param reaction:
    #     :param challenger:
    #     :return:
    #     """
    #     opponent = ""
    #     if reaction.message.author.id == bot.user.id and not challenger.id == bot.user.id:
    #         move = constant.BUTTON_DECODER[(str(reaction.emoji))]
    #         if move is not None:
    #             await self.game_handler(challenger, opponent, reaction.message, move)


if __name__ == '__main__':
    bot = ConnectFourBot("c4 ")
    bot.run(TOKEN)
