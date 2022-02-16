import discord
import os
from discord.ext import commands
from src.game import ConnectFour, PLAYER1, PLAYER2, EMPTY
from time import sleep

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")
CALLSIGN = "c4 "
bot = commands.Bot(command_prefix=CALLSIGN)

PLAYER1_PIECE = ":regional_indicator_x:"
PLAYER2_PIECE = ":o2:"
EMPTY_PIECE = ":white_large_square:"
NUM_PLAYERS = 2
DROP_TIME = 0.0

PIECES = {
    EMPTY: EMPTY_PIECE,
    PLAYER1: PLAYER1_PIECE,
    PLAYER2: PLAYER2_PIECE
}

# BUTTON CONSTANTS
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


@bot.command(name='challenge',
             aliases=['clg'],
             brief='brief',
             description='Challenge a player or agent by providing the ID.  If no parameter is given, then a menu '
                         'will assist.',
             help='help'
             )
async def challenge(ctx, player=None):
    if player is None:
        await ctx.send("Print Default Challenge Dialog")
    else:
        await ctx.send(f"Challenge {player}")


@bot.command(name="leaderboard",
             aliases=['lb'],
             brief='brief',
             description='Display the record for a player or agent by providing the ID. If no parameter is given, '
                         'then a default leaderboard will be displayed.',
             help='help'
             )
async def leaderboard(ctx, player=None):
    if player is None:
        await ctx.send("Print Default Leaderboard")
    else:
        await ctx.send(f"Display {player}'s Record")


class ConnectFourBot:
    def __init__(self, bot):
        self.bot = bot
        self.games = {}
        self.last_moves = {}
        self.agent1 = {}
        self.agent2 = {}

    @commands.command(pass_context=True)
    async def cfb(self, ctx):
        """Connect Four"""
        await self.cfb_new(ctx.message.author, ctx.message.channel)

    async def cfb_new(self, user, channel):
        response = self.make_board(user)
        response += "Your move:"
        msg = await self.bot.send_message(channel, response)
        await self.make_buttons(msg)

    async def make_buttons(self, msg):
        await self.bot.add_reaction(msg, ONE)
        await self.bot.add_reaction(msg, TWO)
        await self.bot.add_reaction(msg, THREE)
        await self.bot.add_reaction(msg, FOUR)
        await self.bot.add_reaction(msg, FIVE)
        await self.bot.add_reaction(msg, SIX)
        await self.bot.add_reaction(msg, SEVEN)

    def make_board(self, user):
        game = self.games[user]
        representation = ""
        for y in range(game.get_board().height - 1, -1, -1):
            for x in range(game.get_board().width):
                piece = game.get_board().get_piece((x, y))
                representation += f"[{PIECES[piece]}]"
            representation += "\n"
        return representation[:-1]

    async def game_handler(self, user):
        representation = self.make_board(user)

        game = self.games[user]

        if game.turn % NUM_PLAYERS == 0:
            self.last_moves[user] = self.agent1[user].get_action(game)
            sleep(DROP_TIME)
        else:
            self.last_moves[user] = self.agent2[user].get_action(game)
            sleep(DROP_TIME)

    async def challenge_handler(self):
        pass

    async def leaderboard_handler(self):
        pass


bot.run(DISCORD_TOKEN)
