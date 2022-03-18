import discord_bot.constants_discord as constant
from discord.ext import commands
from random import shuffle
from src.game import ConnectFour
from intelligence.agent import Agent
import discord
import time
import uuid


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
        users = list([user.name+"\n" for user in ctx.guild.members])
        await ctx.send(f"Possible Opponents: \n{''.join(users)}")

    async def new_game(self, player1: Agent, player2: Agent):
        """
        Initializes new entry in registry (maps id to game instance data) and legend (maps players to id)
        :param player1: Agent Object which handles interaction
        :param player2: Agent Object which handles interaction
        :return: id where game, player1, player2 is stored.
        """
        # Shuffle Players
        players = [player1, player2]
        shuffle(players)
        id = uuid.uuid1()
        player1, player2 = players
        game = ConnectFour()

        self.registry[id] = {'game': game, 'player1': player1, 'player2': player2}
        self.legend[str(player1)+str(player2)] = id
        return id

    @commands.command(name="setstatus")
    async def setstatus(self, ctx: commands.Context, *, text: str):
        """Set the bot's status."""
        await self.bot.change_presence(activity=discord.Game(name=text))

    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context):
        """Get the bot's current websocket latency"""
        start_time = time.time()
        message = await ctx.send("Testing Ping...")
        end_time = time.time()
        await message.edit(content=f"Pong! {round(self.bot.latency * 1000)}ms\nAPI: {round((end_time - start_time) * 1000)}ms")


def setup(bot: commands.Bot):
    bot.add_cog(ChallengeHandler(bot))


intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
setup(bot)
# bot.load_extension('ChallengeHandler')
TOKEN = "OTU0NDM0ODc1ODMyODE5Nzcy.YjTEvg.ZR2TAXYP_g7WG62cyG04r5o9mRY"
bot.run(TOKEN)
