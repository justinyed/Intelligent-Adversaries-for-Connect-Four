import discord
import os
from discord.ext import commands
from game import ConnectFour, PLAYER1, PLAYER2, EMPTY
from time import sleep

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")
CALLSIGN = "c4 "
bot = commands.Bot(command_prefix=CALLSIGN)

# ### CONSTANTS ###
PLAYER1_PIECE = ":regional_indicator_x:"
PLAYER2_PIECE = ":o2:"
EMPTY_PIECE = ":white_large_square:"
NUM_PLAYERS = 2
DROP_TIME = 0.0
ILLEGAL_INPUT_MSG = ""
BAD_INPUT_TIME = 0.7

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


# This event triggers when your bot
# allows the bot to sit in a ready state and wait for calls.
@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    print(
        f"{bot.user} is connected to the following guild:\n"
        f"{guild.name}(id: {guild.id})"
    )


class ConnectFourBot:
    def __init__(self, bot):
        self.bot = bot
        self.games = {}
        self.last_moves = {}
        self.agent1 = {}
        self.agent2 = {}

    @bot.command(name='challenge',
                 aliases=['clg'],
                 brief='brief',
                 description='Challenge a player or agent by providing the ID.  If no parameter is given, then a menu '
                             'will assist.',
                 help='help'
                 )
    async def challenge(self, ctx, opponent=None):
        if opponent is None:  # Normally print dialog and request more info
            opponent = "Alpha-Beta Agent"
            await self.cfb_new(ctx.message.author, opponent, ctx.message.channel)
        else:
            await ctx.send(f"Challenge {opponent}")

    async def cfb_new(self, challenger, opponent, channel):
        self.games[challenger.id] = None
        response = self.assemble_board(challenger)
        response += "Your move:"
        msg = await self.bot.send_message(channel, response)
        await self.assemble_buttons(msg)

    async def game_handler(self, challenger, opponent, message, move):
        # SETUP
        print("ttt_move:{0}".format(challenger.id))
        uid = challenger.id
        if uid not in self.games:
            print("New game")
            return await self.cfb_new(challenger, opponent, message.channel)
        game = self.games[challenger]

        # DISPLAY BOARD
        self.assemble_board(challenger)

        # REQUEST MOVE
        try:
            if game._turn % NUM_PLAYERS == 0:
                self.last_moves[challenger] = self.agent1[challenger].get_action(game)
                sleep(DROP_TIME)
            else:
                self.last_moves[challenger] = self.agent2[challenger].get_action(game)
                sleep(DROP_TIME)

        except (ValueError, TypeError):
            print(ILLEGAL_INPUT_MSG)
            sleep(BAD_INPUT_TIME)
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

    async def assemble_buttons(self, msg):
        for n in BUTTON_NUMBERS:
            await self.bot.add_reaction(msg, n)

    async def on_reaction_add(self, reaction, challenger):
        opponent = ""
        if reaction.message.author.id == self.bot.user.id and not challenger.id == self.bot.user.id:
            move = BUTTON_DECODER[(str(reaction.emoji))]
            if move is not None:
                await self.game_handler(challenger, opponent, reaction.message, move)

    def assemble_board(self, user):
        game = self.games[user]
        representation = ""
        for y in range(game.get_board().height - 1, -1, -1):
            for x in range(game.get_board().width):
                piece = game.get_board().get_piece((x, y))
                representation += f"[{PIECES[piece]}]"
            representation += "\n"
        return representation[:-1]

    # @bot.command(name="leaderboard",
    #              aliases=['lb'],
    #              brief='brief',
    #              description='Display the record for a player or agent by providing the ID. If no parameter is given, '
    #                          'then a default leaderboard will be displayed.',
    #              help='help'
    #              )
    # async def leaderboard(self, ctx, player=None):
    #     if player is None:
    #         await ctx.send("Print Default Leaderboard")
    #     else:
    #         await ctx.send(f"Display {player}'s Record")


def setup(bot):
    bot.add_cog(ConnectFourBot(bot))


setup(bot)
bot.run(DISCORD_TOKEN)
