import uuid
from random import shuffle
import discord
from discord.ext import commands
import asyncio
import discord_bot.discord_config as config
from discord_bot.discord_config import MESSAGE, TIME
import game_components


class ChallengeHandler(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.leaderboard_handler = None
        print("[ChallengeHandler Initialized]")

    @commands.command(name='challenge', aliases=['clg'],
                      description=config.CLG_DESCRIPTION, help='help', pass_contaxt=True)
    async def challenge(self, ctx: commands.Context, opponent=None):
        """
        Allows the player to challenge an opponent
        :param ctx: context
        :param opponent: opponent player to challenge; if none options are given.
        """
        msg = await ctx.send(MESSAGE.welcome)
        challenger = ctx.author

        # Direct Agent Selection?
        if opponent is None:
            opponent = await self._agent_selection(msg, ctx.author)
        elif opponent.replace("@", "") in config.AGENTS.keys():
            opponent = opponent.replace("@", "")
        else:
            opponent = await self.bot.fetch_user(opponent.strip("<@!>"))

            # Challenged Bot?
            if opponent.display_name == self.bot.user.display_name:
                opponent = await self._agent_selection(msg, ctx.author)

            # Challenged Self?
            elif opponent == challenger:
                await ctx.send(MESSAGE.tell_challenger_self(challenger), delete_after=5)
                return

            # Challenged Other Player?
            elif not await self._challenge_check(msg, challenger, opponent):
                return

        await self._game_handler(msg, *await self._new_game(challenger, opponent))

    async def _challenge_check(self, msg: discord.Message, challenger, opponent):
        """
        verify opponent, ask for opponent to accept
        :param msg:
        :param challenger:
        :param opponent:
        :return:
        """
        # query opponent
        await msg.edit(
            content=MESSAGE.tell_challenge(challenger.display_name, opponent.mention),
            components=config.ACCEPT_REJECT_BUTTONS
        )

        # handle button press
        try:
            interaction, button = await self.bot.wait_for(
                'button_click', check=lambda i, b: i.message == msg and i.user_id == opponent.id,
                timeout=TIME.challenge_timeout
            )

            await interaction.defer()

            # check for rejection
            if button.custom_id == "reject":
                await msg.edit(
                    content=MESSAGE.tell_challenger_declined(opponent.display_name),
                    components=[],
                    delete_after=TIME.rejection_timeout
                )
                return False
            else:
                return True

        except asyncio.TimeoutError:
            await msg.edit(
                content=MESSAGE.tell_challenger_timed_out(opponent.display_name),
                components=[],
                delete_after=TIME.challenge_timeout_message
            )
            return False

    async def _game_handler(self, msg: discord.Message, game, player1, player2, uid):
        """
        Handles turns of game.
        :param msg: message to display to users
        :param game: ConnectFour Game Object
        :param player1: id
        :param player2: id
        :param: uid: unique game id
        """

        if game.is_terminal_state():

            if game.is_tied():
                await self.leaderboard_handler.end_game(uid, str(player1), str(player2), game.get_status(), True)

                e = discord.Embed(title=MESSAGE.tie)
                await msg.edit(content=ChallengeHandler._assemble_board(game), embed=e, components=[])

            if game.is_won():
                # update leaderboard
                winner = str(self.current_player(game, player1, player2))
                loser = str(self.other_player(game, player1, player2))

                await self.leaderboard_handler.end_game(uid, winner, loser, game.get_status())

                e = discord.Embed(
                    title=MESSAGE.tell_winner(ChallengeHandler.current_player_name(game, player1, player2))
                )
                await msg.edit(content=ChallengeHandler._assemble_board(game), embed=e, components=[])

            return

        def check_button(i: discord.Interaction, b: discord.Button):
            if not (i.message == msg and i.user_id == ChallengeHandler.current_player(game, player1, player2).id):
                return False
            if b.custom_id == config.FORFEIT:
                return True
            return (int(b.custom_id) - 1) in game.get_legal_actions()

        await ChallengeHandler._update_display(msg, game, player1, player2)

        current_player = ChallengeHandler.current_player_name(game, player1, player2)

        if current_player in config.AGENTS.keys():
            await asyncio.sleep(0.3)  # Yield control
            action = config.AGENTS[current_player].get_action(game)
        else:
            interaction, button = await self.bot.wait_for('button_click', check=check_button)

            if button.custom_id == config.FORFEIT:  # Forfeit?  # todo - refactor; add stop gap
                quitter = str(self.current_player(game, player1, player2))
                winner = str(self.other_player(game, player1, player2))

                forfeit_msg = f"{quitter} has opted to forfeit the game, {winner} is the Winner!"
                e = discord.Embed(title=forfeit_msg)

                await self.leaderboard_handler.end_game(uid, winner, quitter, 4)
                await msg.edit(content="", embed=e, components=[], delete_after=10)
                return

            action = int(button.custom_id) - 1
            await interaction.defer()

        game.perform_action(action)
        # await self.leaderboard_handler.update_move(uid, action)
        await self._game_handler(msg, game, player1, player2, uid)

    async def _new_game(self, player1, player2):
        """
        Initializes new game and shuffles players
        :param player1: Agent Object which handles interaction
        :param player2: Agent Object which handles interaction
        :return: game, player1, player2
        """
        # Shuffle who starts
        players = [player1, player2]
        shuffle(players)
        player1, player2 = players

        # start game
        game = game_components.ConnectFour()

        # Initialize Leaderboard Entries
        uid = uuid.uuid1()
        await self.leaderboard_handler.add_game(uid, str(player1), str(player2))

        return game, player1, player2, uid

    async def _agent_selection(self, msg: discord.Message, challenger):
        await msg.edit(content=MESSAGE.select_agent, components=config.AGENT_MENU)

        interaction, select_menu = await self.bot.wait_for(
            'selection_select', check=lambda i, b: i.author == challenger and i.message == msg
        )

        await interaction.defer()
        return select_menu.values[0]

    @staticmethod
    async def _update_display(msg: discord.Message, game, player1, player2):
        await msg.edit(
            embed=ChallengeHandler._assemble_display(game, player1, player2),
            content=ChallengeHandler._assemble_board(game),
            components=config.PLAY_BUTTONS
        )

    @staticmethod
    def current_player(game, player1, player2):
        if game.get_current_player() == 1:
            return player1
        else:
            return player2

    @staticmethod
    def other_player(game, player1, player2):
        if game.get_current_player() == -1:
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
        current_player = ChallengeHandler.current_player_name(game, player1, player2)
        current_piece = config.PIECES[game.get_current_player()]
        turn_message = MESSAGE.tell_turn_start(current_player, current_piece)

        embed = discord.Embed()
        embed.add_field(name=turn_message, value=MESSAGE.turn_prompt, inline=False)
        return embed

    @staticmethod
    def _assemble_board(game):
        """
        Create the representation of the game
        :param game: game state
        :return: string representation of the game
        """
        # header
        representation = "\n" + config.structure + "".join(config.DISPLAY_NUMBERS) + config.structure + "\n"

        # board
        for y in range(game.get_board().get_height() - 1, -1, -1):
            representation += config.structure

            for x in range(game.get_board().get_width()):
                piece = game.get_board().get_piece((x, y))
                representation += config.PIECES[piece]

            representation += config.structure + "\n"
        return representation + config.structure * 9

    @staticmethod
    def setup(bot: commands.Bot, leaderboard_handler):
        ch = ChallengeHandler(bot)
        bot.add_cog(ch)
        ch.leaderboard_handler = leaderboard_handler

    @commands.command(name='demonstration', aliases=['demo'], pass_contaxt=True)
    async def demo(self, ctx: commands.Context, agent1='Hard', agent2=None, iterations=100):
        """
        Starts Demo Between Two Agents
        """
        if str(ctx.author) not in config.ADMINS:
            await ctx.send("You do not have permission for this command", delete_after=3)
            return

        msg = await ctx.send(MESSAGE.welcome)
        agent1 = agent1.replace("@", "").replace(" ", "")

        if agent2 is None or agent2 == "''":
            agent2 = agent1
        for i in range(iterations):
            print(f"Started Demonstration({i}) between \"{agent1}\" and \"{agent2}\"")
            await self._game_handler(msg, *await self._new_game(agent1, agent2))
            await asyncio.sleep(5)

