import os
import time
from random import shuffle
import discord
from discord.ext import commands
from discord import Button, ButtonStyle, ActionRow, SelectMenu, SelectOption
import discord_bot.constants_discord as constant
from discord_bot.util import Util
from src.game import ConnectFour
import intelligence

buttons1 = ActionRow(*list([Button(label=f"{i}", custom_id=f"{i}", style=ButtonStyle.red) for i in range(1, 4)]))
buttons2 = ActionRow(*list([Button(label=f"{i}", custom_id=f"{i}", style=ButtonStyle.red) for i in range(4, 8)]))
structure = ":blue_square:"


class ChallengeHandler(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
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
            msg = await ctx.send("Welcome to Connect Four!")
            await self.game_handler(msg, *await self.new_game(ctx.author, 'AlphaBeta Agent'))

    async def new_game(self, player1, player2):
        """
        Initializes new entry in registry (maps gid to game instance data) and legend (maps players to gid)
        :param player1: Agent Object which handles interaction
        :param player2: Agent Object which handles interaction
        :return: gid where game, player1, player2 is stored.
        """

        # Shuffle Players
        players = [player1, player2]
        # shuffle(players)
        player1, player2 = players
        game = ConnectFour()

        return game, player1, player2

    async def game_handler(self, msg: discord.Message, game, player1, player2):
        """
        Handles turns of game
        :return:
        """
        await msg.edit(embed=self.assemble_display(game, player1, player2), content="\n"+ChallengeHandler.assemble_board(game), components=[buttons1, buttons2])

        if game.get_turn() % constant.NUM_PLAYERS == 0:
            interaction, button = await self.bot.wait_for('button_click')
            action = int(button.custom_id) - 1
            await interaction.respond(f"Drop in Column {action+1}", delete_after=0.000000001)

        else:
            a = intelligence.AlphaBeta(player=-1)
            action = a.get_action(game)

        game.perform_action(action)

        if game.is_terminal_state():
            if game.is_tie():
                await msg.edit(embed=discord.Embed(title="Connect Four",
                                                   description=f"The game has been Tied."))
                await msg.delete(delay=15)
                return
            else:  # winner
                await msg.edit(embed=discord.Embed(title="Connect Four",
                                                   description=f"{ChallengeHandler.current_player(game, player1, player2)} has Triumphed!"))
                await msg.delete(delay=15)
                return

        await self.game_handler(msg, game, player1, player2)

    @staticmethod
    def current_player(game, player1, player2):
        if game.get_current_player() == -1:
            return player2
        else:
            return player1

    def assemble_display(self, game, player1, player2):
        embed = discord.Embed().add_field(name="Play", value=f"It is {self.current_player(game, player1, player2)}'s turn.", inline=False)
        return embed

    @staticmethod
    def assemble_board(game):
        """
        Create the representation of the game
        :param game: game state
        :return: string representation of the game
        """
        representation = structure + "".join(constant.BUTTON_NUMBERS) + structure + "\n"
        for y in range(game.get_board().get_height() - 1, -1, -1):
            representation += structure
            for x in range(game.get_board().get_width()):
                piece = game.get_board().get_piece((x, y))
                representation += f"{constant.PIECES[piece]}"
            representation += f"{structure}\n"
        return representation + structure * 9

    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context):
        """Get the bot's current websocket latency"""
        start_time = time.time()
        message = await ctx.send("Testing Ping...")
        end_time = time.time()
        await message.edit(
            content=f"Online! {round(self.bot.latency * 1000)}ms\nAPI: {round((end_time - start_time) * 1000)}ms")


def setup(bot: commands.Bot):
    bot.add_cog(ChallengeHandler(bot))


intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
setup(bot)
TOKEN = Util.read_json_from_file("./discord_bot/connect_four_config.json")['Token']
bot.run(TOKEN)
