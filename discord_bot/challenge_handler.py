import os

import discord_bot.constants_discord as constant
from discord.ext import commands
from discord import embeds
import discord
from random import shuffle
from src.game import ConnectFour
from discord import Button, ButtonStyle, ActionRow, SelectMenu, SelectOption, Emoji
from intelligence.agent import Agent
import intelligence
import time
import uuid
from util import Util


G, P1, P2, LM = 'game', 'player1', 'player2', 'last_move'


class ChallengeHandler(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.registry = {}
        self.legend = {}
        print("[ChallengeHandler Initialized]")

    @commands.command()
    async def buttons(self, ctx: commands.Context):

        buttons1 = ActionRow(*list([Button(label=f"{i}", custom_id=f"{i}", style=ButtonStyle.red) for i in range(1, 4)]))
        buttons2 = ActionRow(*list([Button(label=f"{i}", custom_id=f"{i}", style=ButtonStyle.red) for i in range(4, 8)]))
        msg_with_buttons = await ctx.send('Hey here are some Buttons', components=[buttons1, buttons2])

        def check_button(interaction: discord.Interaction, button):
            return interaction.author == ctx.author and interaction.message == msg_with_buttons

        interaction, button = await self.bot.wait_for('button_click', check=check_button)

        embed = discord.Embed(title='You pressed a Button',
                              description=f'You pressed a {button.custom_id} button.',
                              color=discord.Color.random())
        await interaction.respond(embed=embed)

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

    async def new_game(self, player1, player2):
        """
        Initializes new entry in registry (maps gid to game instance data) and legend (maps players to gid)
        :param player1: Agent Object which handles interaction
        :param player2: Agent Object which handles interaction
        :return: gid where game, player1, player2 is stored.
        """
        if player2 == 'bot':
            player2 = intelligence.AlphaBeta(player=-1)

        # Shuffle Players
        players = [player1, player2]
        shuffle(players)
        gid = uuid.uuid1()
        player1, player2 = players
        game = ConnectFour()

        self.registry[gid] = {'game': game, 'player1': player1, 'player2': player2, 'last_move': None}
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

    @commands.command()
    async def select(self, ctx):
        msg_with_selects = await ctx.send('Hey here is an nice Select-Menu', components=[
            [
                SelectMenu(custom_id='_select_it', options=[
                    SelectOption(emoji='1️⃣', label='Option Nr° 1', value='1', description='The first option'),
                    SelectOption(emoji='2️⃣', label='Option Nr° 2', value='2', description='The second option'),
                    SelectOption(emoji='3️⃣', label='Option Nr° 3', value='3', description='The third option'),
                    SelectOption(emoji='4️⃣', label='Option Nr° 4', value='4', description='The fourth option')],
                           placeholder='Select some Options', max_values=3)
            ]])

        def check_selection(i: discord.Interaction, select_menu):
            return i.author == ctx.author and i.message == msg_with_selects

        interaction, select_menu = await self.bot.wait_for('selection_select', check=check_selection)

        embed = discord.Embed(title='You have chosen:',
                              description=f"You have chosen " + '\n'.join(
                                  [f'\nOption Nr° {o}' for o in select_menu.values]),
                              color=discord.Color.random())
        await interaction.respond(embed=embed)

    async def game_handler(self, msg: discord.Message, gid):
        """
        Handles turns of game
        :return:
        """

        game = self.registry[gid][G]

        await msg.edit(embed=self.assemble_display(gid))

        if game.get_turn() % constant.NUM_PLAYERS == 0:
            self.registry[gid][LM] = self.registry[gid][P1].get_action(game)
        else:
            self.registry[gid][LM] = self.registry[gid][P2].get_action(game)

        game.perform_action(self.registry[gid][LM])

        if game.is_terminal_state():
            if game.is_tie():
                pass
            else:
                winning_player = game.get_current_player()
                pass

        self.registry[gid][G] = game
        await self.game_handler(msg, gid)

    def assemble_display(self, gid):
        embed = discord.Embed(title="Connect Four", description=ChallengeHandler.assemble_board(self.registry[gid][G]))
        embed.set_author(name=f"{self.registry[gid][P1]} vs {self.registry[gid][P2]}")
        embed.add_field(name="Turn", value=self.registry[gid][G].get_turn(), inline=True)
        embed.add_field(name="Status", value=self.registry[gid][G].get_status(), inline=True)
        embed.add_field(name="Play", value=f"It is {self.registry[gid][G].get_current_player()}'s turn.", inline=False)
        return embed

    @staticmethod
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

    async def assemble_buttons(self, msg: discord.Message):
        """
        Create reaction buttons
        :param msg:
        :return:
        """
        for button in constant.BUTTON_NUMBERS:
            await msg.add_reaction(button)

    async def on_reaction_add(self, reaction, user):
        """

        :param reaction:
        :param challenger:
        :return:
        """
        opponent = ""
        if reaction.message.author.id == bot.user.id and not user.id == bot.user.id:
            move = constant.BUTTON_DECODER[(str(reaction.emoji))]
            if move is not None:
                return move


def setup(bot: commands.Bot):
    bot.add_cog(ChallengeHandler(bot))


intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
setup(bot)
TOKEN = Util.read_json_from_file("./discord_bot/connect_four_config.json")['Token']
bot.run(TOKEN)
