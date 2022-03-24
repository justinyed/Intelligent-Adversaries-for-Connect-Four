from random import shuffle
import discord
import asyncio
from discord.ext import commands
from discord import Button, ButtonStyle, ActionRow, SelectMenu, SelectOption
import discord_bot.constants_discord as constant
from src.game import ConnectFour


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
        msg = await ctx.send("Welcome to Connect Four!")
        challenger = ctx.author

        if opponent is None:  # Agent Selection
            opponent = await self._agent_selection(msg, ctx.author)
        else:
            opponent = await self.bot.fetch_user(opponent.strip("<@!>"))
            if opponent.display_name == self.bot.user.display_name:
                opponent = await self._agent_selection(msg, ctx.author)
            else:
                if not await self._challenge_check(msg, challenger, opponent):
                    return

        await self._game_handler(msg, *await ChallengeHandler._new_game(challenger, opponent))

    async def _challenge_check(self, msg: discord.Message, challenger, opponent):
        """
        verify opponent, ask for opponent to accept
        :param msg:
        :param challenger:
        :param opponent:
        :return:
        """
        await msg.edit(
            content=f"{opponent.mention}, {challenger.display_name} has challenged you to a Connect Four Match.",
            components=constant.ACCEPT_REJECT_BUTTONS
        )

        try:
            interaction, button = await \
                self.bot.wait_for('button_click', check=lambda i, b: i.message == msg and i.user_id == opponent.id, timeout=15)
            await interaction.defer()

            # check for rejection
            if button.custom_id == "reject":
                await msg.edit(content=f"{opponent.display_name} has rejected the challenge.",
                               components=[],
                               delete_after=5)
                return False
            else:
                return True
        except asyncio.TimeoutError:
            await msg.edit(content=f"{opponent.display_name} has not responded to the challenge.",
                           components=[],
                           delete_after=5)
            return False

    async def _game_handler(self, msg: discord.Message, game, player1, player2):
        """
        Handles turns of game
        :param msg: message to display to users
        :param game: ConnectFour Game Object
        :param player1: id
        :param player2: id
        """
        if game.is_terminal_state():
            if game.is_tie():
                e = discord.Embed(title=f"The game has been Tied.")
                await msg.edit(content=ChallengeHandler._assemble_board(game), embed=e, components=[], delete_after=15)
                return
            else:  # winner
                e = discord.Embed(
                    title=f"{ChallengeHandler.current_player_name(game, player1, player2)} has Triumphed!")
                await msg.edit(content=ChallengeHandler._assemble_board(game), embed=e, components=[], delete_after=15)
                return

        def check_button(i: discord.Interaction, b: discord.Button):
            if not (i.message == msg and i.user_id == ChallengeHandler.current_player(game, player1, player2).id):
                return False
            return (int(b.custom_id) - 1) in game.get_legal_actions()

        await ChallengeHandler._update_display(msg, game, player1, player2)

        current_player = ChallengeHandler.current_player_name(game, player1, player2)

        if current_player in constant.AGENTS.keys():
            action = constant.AGENTS[current_player].get_action(game)
        else:
            interaction, button = await self.bot.wait_for('button_click', check=check_button)
            action = int(button.custom_id) - 1
            await interaction.defer()

        game.perform_action(action)
        await self._game_handler(msg, game, player1, player2)

    @staticmethod
    async def _new_game(player1, player2):
        """
        Initializes new game and shuffles players
        :param player1: Agent Object which handles interaction
        :param player2: Agent Object which handles interaction
        :return: game, player1, player2
        """
        players = [player1, player2]
        shuffle(players)
        player1, player2 = players
        game = ConnectFour()

        return game, player1, player2

    async def _agent_selection(self, msg: discord.Message, challenger):
        await msg.edit(content='Select an Artificially Intelligent Adversary', components=constant.AGENT_MENU)
        interaction, select_menu = await \
            self.bot.wait_for('selection_select', check=lambda i, b: i.author == challenger and i.message == msg)
        await interaction.defer()
        return select_menu.values[0]

    @staticmethod
    async def _update_display(msg: discord.Message, game, player1, player2):
        await msg.edit(embed=ChallengeHandler._assemble_display(game, player1, player2),
                       content=ChallengeHandler._assemble_board(game), components=constant.BUTTONS)

    @staticmethod
    def current_player(game, player1, player2):
        if game.get_current_player() == 1:
            return player1
        else:
            return player2

    @staticmethod
    def current_player_name(game, player1, player2):
        p = ChallengeHandler.current_player(game, player1, player2)
        if type(p) is not str:
            return p.display_name
        else:
            return p

    @staticmethod
    def _assemble_display(game, player1, player2):
        embed = discord.Embed()
        n = f"It is {ChallengeHandler.current_player_name(game, player1, player2)}'s ( {constant.PIECES[game.get_current_player()]} ) turn."
        embed.add_field(name=n, value="Make a Selection", inline=False)
        return embed

    @staticmethod
    def _assemble_board(game):
        """
        Create the representation of the game
        :param game: game state
        :return: string representation of the game
        """
        representation = "\n" + constant.structure + "".join(constant.BUTTON_NUMBERS) + constant.structure + "\n"
        for y in range(game.get_board().get_height() - 1, -1, -1):
            representation += constant.structure
            for x in range(game.get_board().get_width()):
                piece = game.get_board().get_piece((x, y))
                representation += f"{constant.PIECES[piece]}"
            representation += f"{constant.structure}\n"
        return representation + constant.structure * 9

    @staticmethod
    def setup(bot: commands.Bot):
        bot.add_cog(ChallengeHandler(bot))
