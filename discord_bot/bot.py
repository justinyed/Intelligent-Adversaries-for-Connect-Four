import discord_bot.constants_discord as constant
from discord.ext import commands
from random import shuffle
from src.game import ConnectFour
from intelligence.agent import Agent
import discord
import time
import uuid
from discord import embeds

G, P1, P2 = 'game', 'player1', 'player2'


def assemble_board(game):
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


class ChallengeHandler(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.registry = {}
        self.legend = {}
        print("[ChallengeHandler Initialized]")

    @commands.command(name='challenge', aliases=['clg'],
                      description=constant.CLG_DESCRIPTION, help='help', pass_contaxt=True)
    async def challenge(self, ctx: commands.Context, opponent=None):
        """
        Allows the player to challenge an opponent
        :param ctx: context
        :param opponent: opponent player to challenge; if none options are given.
        """
        if opponent is not None:
            await ctx.send(f"New Challenge: {ctx.author} challenges {opponent}")
        else:
            await self.opponent_selection(ctx)

    async def opponent_selection(self, ctx: commands.Context):
        users = list([user.name + "\n" for user in ctx.guild.members])
        await ctx.send(f"Possible Opponents: \n{''.join(users)}")

    async def new_game(self, player1: Agent, player2: Agent):
        """
        Initializes new entry in registry (maps gid to game instance data) and legend (maps players to gid)
        :param player1: Agent Object which handles interaction
        :param player2: Agent Object which handles interaction
        :return: gid where game, player1, player2 is stored.
        """
        # Shuffle Players
        players = [player1, player2]
        shuffle(players)
        gid = uuid.uuid1()
        player1, player2 = players
        game = ConnectFour()

        self.registry[gid] = {'game': game, 'player1': player1, 'player2': player2}
        self.legend[str(player1) + str(player2)] = gid
        return gid

    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context):
        """Get the bot's current websocket latency"""
        start_time = time.time()
        message = await ctx.send("Testing Ping...")
        end_time = time.time()
        await message.edit(
            content=f"Pong! {round(self.bot.latency * 1000)}ms\nAPI: {round((end_time - start_time) * 1000)}ms")

    async def game_handler(self, msg: discord.Message, gid):
        """
        Handles turns of game
        :return:
        """

        game = self.registry[gid][G]
        player1 = self.registry[gid][P1]
        player2 = self.registry[gid][P2]

        # DISPLAY BOARD
        await msg.edit(embed=self.assemble_display(gid))

        try:
            # REQUEST MOVE
            if game.get_turn() % constant.NUM_PLAYERS == 0:
                last_move = player1.get_action(game)
            else:
                last_move = player2.get_action(game)

            # MAKE MOVE
            game.perform_action(last_move)

        except (ValueError, TypeError):
            print(constant.ILLEGAL_INPUT_MSG)
            await self.game_handler(msg, gid)

            # CHECK TERMINAL STATE
            if game.is_tie():  # TIE
                pass
            elif game.is_terminal_state():
                winning_player = game.get_current_player()
                pass
        # LOOP
        await self.game_handler(msg, gid)

    def assemble_display(self, gid):
        embed = discord.Embed(title="Connect Four", description=assemble_board(self.registry[gid][G]))
        embed.set_author(name=f"{self.registry[gid][P1]} vs {self.registry[gid][P2]}")
        embed.add_field(name="Turn", value=self.registry[gid][G].get_turn(), inline=True)
        embed.add_field(name="Status", value=self.registry[gid][G].get_status(), inline=True)
        embed.add_field(name="Play", value=f"It is {self.registry[gid][G].get_current_player()}'s turn.", inline=False)
        return embed


def setup(bot: commands.Bot):
    bot.add_cog(ChallengeHandler(bot))


intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
setup(bot)
# bot.load_extension('ChallengeHandler')
TOKEN = ""
bot.run(TOKEN)
